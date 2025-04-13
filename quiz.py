import pyttsx3
import speech_recognition as sr
import time
import os
import random

# Initialize TTS engine
NUM_QUESTIONS=3
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_speech_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your answer (say option A, B, C, or D)...")
        start_time = time.time()
        audio = r.listen(source, phrase_time_limit=30)  # Limit listening time

    try:
        response = r.recognize_google(audio)
        print("You said:", response)
        speak("say confirm to lock your answer")

        with sr.Microphone() as confirm_source:
            confirm_audio = r.listen(confirm_source, phrase_time_limit=5)

        confirmation = r.recognize_google(confirm_audio)
        print("Confirmation:", confirmation)

        if confirmation.lower() == "confirm":
            return response.lower(), time.time() - start_time
        else:
            speak("Okay, let's try again.")
            return get_speech_input()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        speak("Sorry, I couldn't understand that.")
        return get_speech_input()
    except sr.RequestError:
        print("Could not request results. Please check your internet connection.")
        speak("There was a problem with the internet connection.")
        return "", 30

def get_speech_input2():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your answer")
        audio = r.listen(source)

    try:
        response = r.recognize_google(audio)
        print("You said:", response)
        speak("say confirm to lock your answer")

        with sr.Microphone() as confirm_source:
            confirm_audio = r.listen(confirm_source)

        confirmation = r.recognize_google(confirm_audio)
        print("Confirmation:", confirmation)

        if confirmation.lower() == "confirm":
            return response.lower()
        else:
            speak("Okay, let's try again.")
            return get_speech_input2()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        speak("Sorry, I couldn't understand that.")
        return get_speech_input2()
    except sr.RequestError:
        print("Could not request results. Please check your internet connection.")
        speak("There was a problem with the internet connection.")
        return ""

quizx = [
    {
        "question": "What is the largest mammal in the world?",
        "options": ["A. Elephant", "B. Blue Whale", "C. Giraffe", "D. Hippopotamus"],
        "answer": "option b"
    },
    {
        "question": "Who wrote the play 'Romeo and Juliet'?",
        "options": ["A. Charles Dickens", "B. Jane Austen", "C. William Shakespeare", "D. Mark Twain"],
        "answer": "option c"
    },
    {
        "question": "What gas do plants absorb from the atmosphere?",
        "options": ["A. Oxygen", "B. Nitrogen", "C. Carbon Dioxide", "D. Hydrogen"],
        "answer": "option c"
    },
    {
        "question": "How many continents are there on Earth?",
        "options": ["A. 5", "B. 6", "C. 7", "D. 8"],
        "answer": "option c"
    },
    {
        "question": "Which language is used to style web pages?",
        "options": ["A. HTML", "B. Python", "C. CSS", "D. Java"],
        "answer": "option c"
    },
    {
        "question": "In which country is the Great Pyramid of Giza located?",
        "options": ["A. Mexico", "B. India", "C. Egypt", "D. Peru"],
        "answer": "option c"
    },
    {
        "question": "What is the chemical symbol for Gold?",
        "options": ["A. Au", "B. Ag", "C. Go", "D. Gd"],
        "answer": "option a"
    },
    {
        "question": "Who was the first person to walk on the Moon?",
        "options": ["A. Yuri Gagarin", "B. Buzz Aldrin", "C. Neil Armstrong", "D. Michael Collins"],
        "answer": "option c"
    },
    {
        "question": "Which organ in the human body pumps blood?",
        "options": ["A. Brain", "B. Liver", "C. Heart", "D. Lungs"],
        "answer": "option c"
    },
    {
        "question": "Which is the smallest prime number?",
        "options": ["A. 0", "B. 1", "C. 2", "D. 3"],
        "answer": "option c"
    }
]

rList = random.sample(range(0, 10), NUM_QUESTIONS)
quiz = [quizx[i] for i in rList]

def save_score(name, score):
    with open("leaderboard.txt", "a") as file:
        file.write(f"{name}:{score:.2f}\n")

def show_leaderboard():
    print("\n--- Leaderboard ---")
    if not os.path.exists("leaderboard.txt"):
        print("No scores yet.")
        return

    with open("leaderboard.txt", "r") as file:
        scores = [line.strip().split(":") for line in file if ":" in line]
        scores = [(name, float(score)) for name, score in scores]
        scores.sort(key=lambda x: x[1], reverse=True)

        for i, (name, score) in enumerate(scores[:5], start=1):
            print(f"{i}. {name} - {score:.2f}")

def text_mode():
    score = 0
    for q in quiz:
        print("\nQuestion:", q["question"])
        for opt in q["options"]:
            print(opt)
        start_time = time.time()
        user_answer = input("Your answer (A/B/C/D): ").strip().lower()
        elapsed = time.time() - start_time
        ex_ans = "option " + user_answer
        if ex_ans == q["answer"]:
            bonus = max(0, (30 - elapsed) / 30)
            gained = 1 + bonus
            print(f"Correct! +{gained:.2f} points")
            score += gained
        else:
            print(f"Wrong. The correct answer was: {q['answer']}")
    name = input("\nEnter your name for the leaderboard: ")
    save_score(name, score)
    print(f"Your final score is {score:.2f}/{len(quiz)*2}")
    show_leaderboard()

def voice_mode():
    score = 0
    

    for q in quiz:
        print("\nQuestion:", q["question"])
        speak(q["question"])
        for opt in q["options"]:
            speak(opt)
            print(opt)

        answer, elapsed = get_speech_input()

        if answer== q["answer"]:
            bonus = max(0, (30 - elapsed) / 30)
            gained = 1 + bonus
            speak(f"Correct! You earned {gained:.2f} points")
            print(f"Correct! +{gained:.2f} points")
            score += gained
        else:
            correct_opt = q["answer"]
            speak(f"Wrong. The correct answer was {correct_opt}")
            print(f"Wrong. The correct answer was {correct_opt}")
        time.sleep(1)

    speak(f"Your final score is {score:.2f} out of {len(quiz)*2}")
    print(f"\nYour final score is {score:.2f}/{len(quiz)*2}")

    speak("Please enter your name for the leaderboard.")
    name = get_speech_input2().lower()
    save_score(name, score)
    show_leaderboard()
def show_instructions(mode):
    print("\n📜 INSTRUCTIONS 📜")
    if mode == "1":
        print(f"- {NUM_QUESTIONS} questions total.")
        print("- You have 30 seconds per question.")
        print("- Press a-d to select an option.")
        
        print("- Bonus points if you answer faster.")
        
        
    else:
        speak("Welcome to the voice quiz.")
        print("Welcome to the voice quiz.")

        speak(f"There will be {NUM_QUESTIONS} questions.")
        print(f"There will be {NUM_QUESTIONS} questions.")

        speak("You have 30 seconds to answer each.")
        print("You have 30 seconds to answer each.")

        

        speak("The faster you answer, the more you score.")
        print("The faster you answer, the more you score.")

        
        time.sleep(2)
def main():
    print("Welcome to the Quiz Application!")
    print("Select Mode:")
    print("1. Text Mode")
    print("2. Voice Mode")
    mode = input("Enter 1 or 2: ").strip()
    show_instructions(mode)
    if mode == "1":
        text_mode()
    elif mode == "2":
        voice_mode()
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()