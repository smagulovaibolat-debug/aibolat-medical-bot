if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Bot is running!"

    import threading
    threading.Thread(target=bot.infinity_polling).start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
