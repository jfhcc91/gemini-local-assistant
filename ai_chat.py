import os
import sqlite3
from google import genai
from google.genai import types
from dotenv import load_dotenv  # 👈 FIXED: Changed load_data to load_dotenv

# Load the environment variables from your local hidden file
load_dotenv()  # 👈 FIXED: Changed load_data() to load_dotenv()

# Securely grab the key from your computer's local system environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the official Google client safely
client = genai.Client(api_key=GEMINI_API_KEY)

# ... [The rest of your database and chat loop code remains exactly the same!]

print("==========================================")
print("🚀 Live Gemini Chat Engine Active!")
print("Natively grounded with Live Google Search.")
print("==========================================\n")

def get_database_tasks():
    db_path = "todo.db"
    if not os.path.exists(db_path):
        return "No tasks found."
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, title FROM tasks")
        rows = cursor.fetchall()
        connection.close()
        if not rows: return "To-Do list is empty."
        return "User's current To-Do tasks:\n" + "\n".join([f"- [ID {r[0]}]: {r[1]}" for r in rows])
    except Exception as e:
        return f"DB Error: {e}"

# Start chat tracking using the default flash model
chat = client.chats.create(model="gemini-2.5-flash")

while True:
    user_input = input("✨ You: ")
    if user_input.strip().lower() in ["exit", "quit"]:
        break
        
    if not user_input.strip():
        continue
        
    # Inject database tasks seamlessly if asked
    if any(word in user_input.lower() for word in ["task", "todo", "do to"]):
        db_data = get_database_tasks()
        user_input = f"{db_data}\n\nUser Question: {user_input}"

    print("🤖 Gemini is researching...", end="\r")
    
    # Configure our live Google Search grounding tool
    search_config = types.GenerateContentConfig(
        tools=[{"google_search": {}}]
    )
    
    try:
        # Try processing with our default chat history configuration
        response = chat.send_message(user_input, config=search_config)
        print(" " * 25, end="\r")
        print(f"🤖 AI: {response.text}\n")
        
    except Exception as e:
        # 🚨 TRAFFIC SAFETY INTERCEPT: If the server is overloaded, try the sibling model cluster
        if "503" in str(e) or "UNAVAILABLE" in str(e):
            print("\n🔄 Primary server busy. Routing to alternative model cluster...")
            try:
                # We spin up a single backup request using an alternate model ID
                backup_response = client.models.generate_content(
                    model="gemini-2.5-pro", # Calls the heavy reasoning version instead
                    contents=user_input,
                    config=search_config
                )
                print(f"🤖 AI (Backup Link): {backup_response.text}\n")
            except Exception as backup_error:
                print(f"\n❌ Both Google server pools are full right now: {backup_error}")
        else:
            print(f"\n❌ Error calling Gemini API: {e}")
            break