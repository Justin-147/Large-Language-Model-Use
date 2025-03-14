# A text-based game where you play as a boyfriend trying to apologize to your angry girlfriend.
# Use your communication skills to increase her forgiveness level from 20 to 100 to win,
# but be careful - saying the wrong things can reduce forgiveness to 0 and lose the game.
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import random
import re

# Load environment variables
_ = load_dotenv(find_dotenv())

# Initialize OpenAI client
client = OpenAI()

# Game configuration
INITIAL_FORGIVENESS = 20
WIN_THRESHOLD = 100
LOSE_THRESHOLD = 0

# Predefined reasons for anger
ANGER_REASONS = [
    "You forgot our anniversary",
    "You were looking at other girls",
    "You didn't reply to my messages for hours",
    "You said my best friend looks pretty",
    "You spent more time gaming than with me",
    "You didn't notice my new haircut",
    "You forgot to call me last night",
    "You were late for our date"
]

class AngryGirlfriendGame:
    def __init__(self, reason=None, difficulty='easy'):
        self.forgiveness = INITIAL_FORGIVENESS
        self.reason = reason if reason else random.choice(ANGER_REASONS)
        self.conversation_history = []
        self.game_over = False
        self.difficulty = difficulty
        
        # Adjust system message based on difficulty
        difficulty_prompt = {
            'easy': """You are playing the role of an angry girlfriend who is easy to please. While initially upset, you're very willing to forgive and appreciate your boyfriend's efforts to make things right. You should:
- Be more positive in interpreting his responses
- Give higher scores for genuine attempts to apologize
- Be quick to forgive when he shows sincerity
- Rarely give negative scores unless the response is clearly inappropriate""",
            
            'normal': """You are playing the role of an angry girlfriend with normal emotions. You're upset but reasonable. You should:
- Be balanced in your emotional responses
- Give positive scores for good attempts to make up
- Give negative scores only when responses are insensitive
- Consider the context and effort in the responses""",
            
            'hard': """You are playing the role of an angry girlfriend who is difficult (but not impossible) to please. While very upset, you can still be won over with exceptional responses. You should:
- Be more critical of responses but not unreasonable
- Give positive scores for particularly good answers
- Give negative scores for inadequate or insensitive responses
- Require more effort to be fully convinced"""
        }

        # Score guidelines based on difficulty
        score_guidelines = {
            'easy': """Scoring Guidelines:
* +10: Very sweet or perfectly appropriate response
* +5: Good attempt to make things better
* 0: Neutral or slightly inadequate response
* -5: Only for notably insensitive responses
* -10: Only for extremely inappropriate responses""",

            'normal': """Scoring Guidelines:
* +10: Excellent, very thoughtful response
* +5: Good, sincere attempt
* 0: Neutral or unclear response
* -5: Poor or insensitive response
* -10: Very inappropriate response""",

            'hard': """Scoring Guidelines:
* +10: Exceptional, perfect response
* +5: Very good attempt
* 0: Adequate but not impressive response
* -5: Inadequate response
* -10: Very poor or inappropriate response"""
        }
        
        # Initialize system message
        self.messages = [
            {
                "role": "system",
                "content": f"""{difficulty_prompt[difficulty]}

The player (your boyfriend) has made you angry because: {self.reason}

{score_guidelines[difficulty]}

Format your response EXACTLY as follows (including the brackets):
[EMOTION] Your response text
[SCORE] number

For example:
[UPSET] I'm still a bit upset, but I appreciate your apology.
[SCORE] 5

Remember:
- Stay in character but be consistent with your difficulty level
- Consider the effort and sincerity in each response
- Keep responses concise (1-2 sentences)
- Always use the exact format shown above"""
            }
        ]

    def process_response(self, user_input):
        # Add user input to conversation history
        self.messages.append({"role": "user", "content": user_input})
        
        # Get streaming response from GPT
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            stream=True,
            temperature=0.7
        )

        # Process the response
        full_response = ""
        score = 0
        
        print("\033[35m", end="")  # Purple color for girlfriend's responses
        
        # Collect the full response
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        
        print("\033[0m\n")  # Reset color and add newline
        
        # Extract and calculate score
        try:
            # 使用正则表达式提取分数，匹配 [SCORE] 后面的数字（可能带有+或-号）
            score_match = re.search(r'\[SCORE\]\s*([-+]?\d+)', full_response)
            if score_match:
                # 提取原始分数
                score = int(score_match.group(1))
       
                # 更新原谅值，确保在有效范围内
                self.forgiveness = max(LOSE_THRESHOLD, min(WIN_THRESHOLD, self.forgiveness + score))
            else:
                print("\033[35m[Warning] No score found in response\033[0m")
                print("\033[35m[Score] +0\033[0m")          
        except Exception as e:
            print(f"\033[31m[Error] Score calculation error: {e}\033[0m")
            print("\033[35m[Score] +0\033[0m")
        
        self.messages.append({"role": "assistant", "content": full_response})
        
        # Check win/lose conditions
        if self.forgiveness >= WIN_THRESHOLD:
            self.game_over = True
            return True  # Win
        elif self.forgiveness <= LOSE_THRESHOLD:
            self.game_over = True
            return False  # Lose
        
        return None  # Game continues

    def get_status(self):
        return f"\nForgiveness Score: {self.forgiveness}/100"

def main():
    print("\033[1m=== Angry Girlfriend Game ===\033[0m")
    print("Your girlfriend is angry! Try to make her happy again.")
    
    # Ask for difficulty level
    print("\nChoose difficulty level:")
    print("1. Easy (She's easier to please)")
    print("2. Normal (She has normal emotions)")
    print("3. Hard (She's very difficult to please)")
    
    difficulty_map = {'1': 'easy', '2': 'normal', '3': 'hard'}
    difficulty_choice = input("Enter 1, 2, or 3 (default: 1): ").strip()
    difficulty = difficulty_map.get(difficulty_choice, 'easy')
    
    # Ask if user wants to provide a reason
    print("\nDo you want to specify why she's angry? (y/n)")
    choice = input().lower()
    
    reason = None
    if choice == 'y':
        print("Why is she angry?")
        reason = input()
    
    # Initialize game
    game = AngryGirlfriendGame(reason, difficulty)
    
    print(f"\n\033[31mSituation: {game.reason}\033[0m")
    print(game.get_status())
    
    # Main game loop
    while not game.game_over:
        print("\n\033[32mWhat will you say to her?\033[0m")
        user_input = input()
        
        result = game.process_response(user_input)
        print(game.get_status())
        
        if result is True:
            print("\n\033[32m🎉 Congratulations! She has forgiven you!\033[0m")
            break
        elif result is False:
            print("\n\033[31m💔 Game Over! She broke up with you!\033[0m")
            break

if __name__ == "__main__":
    main() 