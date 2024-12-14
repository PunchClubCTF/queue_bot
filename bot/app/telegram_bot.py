import os
import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from sqlalchemy.orm import sessionmaker
from .models import Student
from . import db, create_app
from flask import current_app

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
REGISTRATION_URL = os.getenv('REGISTRATION_URL', 'https://example.com/register')

# Create bot instance
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to store user registration state
user_registration_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Initialize user registration state
    user_registration_state[message.chat.id] = {
        'telegram_id': message.from_user.id,
        'stage': 'first_name'
    }
    
    # Prompt for first name
    bot.reply_to(message, "Введите ваше имя:")


@bot.message_handler(func=lambda message: message.chat.id in user_registration_state and 
                     user_registration_state[message.chat.id]['stage'] == 'first_name')
def get_first_name(message):
    # Store first name
    user_registration_state[message.chat.id]['first_name'] = message.text
    user_registration_state[message.chat.id]['stage'] = 'last_name'
    
    # Prompt for last name
    bot.reply_to(message, "Отлично! А теперь введите вашу фамилию:")


@bot.message_handler(func=lambda message: message.chat.id in user_registration_state and 
                     user_registration_state[message.chat.id]['stage'] == 'last_name')
def complete_registration(message):
    # Store last name
    user_registration_state[message.chat.id]['last_name'] = message.text
    
    # Extract registration data
    reg_data = user_registration_state[message.chat.id]
    
    # Create database session within app context
    app = create_app()
    with app.app_context():
        try:
            # Check if student already exists
            existing_student = Student.query.filter_by(telegram_id=reg_data['telegram_id']).first()
            
            if not existing_student:
                # Create a new student record
                new_student = Student(
                    telegram_id=reg_data['telegram_id'],
                    name=reg_data['first_name'],
                    surname=reg_data['last_name']
                )
                db.session.add(new_student)
                db.session.commit()
                
                # Send confirmation message
                bot.reply_to(message, f"Регистрация прошла успешно, {reg_data['first_name']} {reg_data['last_name']}.")
            else:
                # Student already exists
                bot.reply_to(message, "Вы уже зарегистрированы. Пожалуйста, используйте команду /start.")
        
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка во время регистрации: {str(e)}")
        
        # Clear registration state
        del user_registration_state[message.chat.id]


def run_bot():
    print("Starting Telegram Bot...")
    bot.polling(none_stop=True)

if __name__ == '__main__':
    run_bot()