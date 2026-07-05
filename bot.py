import os
from threading import Thread
from flask import Flask
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Flask Web Server တည်ဆောက်ခြင်း (Render အတွက်)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Token နှင့် ID များကို လုံခြုံအောင် Environment Variable မှ ဖတ်မည်
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8963413182:AAFJbj2zVbONJhYVTH8m6MMWhthSqwNTQpM")  
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", 7730065663))  

bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}
last_active_user = None  

def get_main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton("🛒 VPN File ဝယ်မည်"), KeyboardButton("💳 Ngwe Hlwal Rant"))
    markup.add(KeyboardButton("📱 အသုံးပြုရမည့် App"), KeyboardButton("📖 ဖိုင်ထည့်နည်း"))
    markup.add(KeyboardButton("📞 ဆက်သွယ်ရန်"))
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 မင်္ဂလာပါ VMT VPN ဝန်ဆောင်မှုမှ ကြိုဆိုပါတယ်။", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.text == "🛒 VPN File ဝယ်မည်")
def buy_vpn(message):
    prices_text = "💵 **VPN စျေးနှုန်းများ ရွေးချယ်ရန်**\n\nကျေးဇူးပြု၍ သက်တမ်းတစ်ခုချင်းစီကို နှိပ်ပါ -"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="🎁 1 Day - Free (အစမ်းသုံး)", callback_data="pack_1Day"))
    markup.add(InlineKeyboardButton(text="🛑 20 Days - 2,500 MMK", callback_data="pack_20"))
    markup.add(InlineKeyboardButton(text="🛑 30 Days - 4,000 MMK", callback_data="pack_30"))
    markup.add(InlineKeyboardButton(text="🛑 40 Days - 5,000 MMK", callback_data="pack_40"))
    bot.send_message(message.chat.id, prices_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("pack_"))
def process_package(call):
    if call.message.chat.id != ADMIN_CHAT_ID:
        pack_name = {"pack_1Day": "1 Day", "pack_20": "20 Days", "pack_30": "30 Days", "pack_40": "40 Days"}[call.data]
        user_states[call.from_user.id] = {"selected_pack": pack_name}
        
        if pack_name == "1 Day":
            bot.send_message(call.message.chat.id, f"✅ သင်ရွေးချယ်ထားသော ပက်ကေ့ချ် - **{pack_name}**\n\nအစမ်းသုံးရန်အတွက် Admin ထံသို့ စာသား (သို့မဟုတ်) Screenshot တစ်ခုခု ပို့ပေးပါ။ Admin က အတည်ပြုပြီး ဖိုင်ပို့ပေးပါလိမ့်မည်။", parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, f"✅ သင်ရွေးချယ်ထားသော ပက်ကေ့ချ် - **{pack_name}**\n\nငွေလွှဲပြီးပါက ပြေစာ Screenshot ကို ဤနေရာတွင် တိုက်ရိုက် ပို့ပေးပါ။", parse_mode="Markdown")
    else:
        global last_active_user
        action = call.data.split("_")
        target_id = int(action[1])
        chosen_pack = action[2]
        
        last_active_user = str(target_id)
        bot.send_message(ADMIN_CHAT_ID, f"🎯 User ID: `{target_id}` ကို အတည်ပြုလိုက်ပါပြီ။ ယခုစာကို Reply နှိပ်၍ VPN File ပို့ပေးနိုင်ပါပြီ။")
        bot.send_message(chat_id=target_id, text=f"🎉 သင့်ရဲ့ **{chosen_pack}** ပြေစာကို Admin က အတည်ပြုလိုက်ပါပြီ။ ခေတ္တစောင့်ဆိုင်းပေးပါ။ Bot ကနေ VPN File အလိုအလျောက် ပို့ပေးပါလိမ့်မည်။")

@bot.message_handler(func=lambda message: message.text in ["💳 Ngwe Hlwal Rant", "💳 Ngwe Hlwal Rant"])
def payment_info(message):
    bot.send_message(message.chat.id, "🏦 **Kpay ( 09.797779790 )**\n\n💸 B-M-T အမည်သို့လွှဲပြီးပါက ပြေစာ ပို့ပေးပါ။")

@bot.message_handler(func=lambda message: message.text == "📱 အသုံးပြုရမည့် App")
def show_app_link(message):
    app_text = (
        "📱 **VPN အသုံးပြုရန် လိုအပ်သော Application များ** 📱\n\n"
        "ကျွန်ုပ်တို့၏ VPN File များကို အသုံးပြုရန်အတွက် အောက်ပါ App ကို ဒေါင်းလုဒ်ဆွဲပြီး အသုံးပြုနိုင်ပါသည်ခင်ဗျာ။\n\n"
        "🤖 **Android အတွက် ဒေါင်းလုဒ်ဆွဲရန် Link:**\n"
        "🔗 [Play Store မှ ဒေါင်းရန် နှိပ်ပါ](https://play.google.com/store/apps/details?id=com.netmod.syna)\n\n"
        "*(Play Store မှ ဒေါင်းမရပါက Admin @vpnserver97 ထံသို့ တိုက်ရိုက်တောင်းယူနိုင်ပါသည်)*"
    )
    bot.send_message(message.chat.id, app_text, parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(func=lambda message: message.text == "📖 ဖိုင်ထည့်နည်း")
def show_tutorial_link(message):
    tutorial_text = (
        "📖 **VPN ဖိုင်ထည့်သွင်း အသုံးပြုနည်း** 📖\n\n"
        "VPN ဖိုင်ထည့်နည်းကို အသေးစိတ် ကြည့်ရှုရန်အတွက် အောက်ပါခလုတ်ကို နှိပ်ပြီး ကျွန်ုပ်တို့၏ **ဖိုင်ထည့်နည်း Channel** ထို့ ဝင်ရောက်လေ့လာနိုင်ပါတယ်ခင်ဗျာ။"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="🚀 ဖိုင်ထည့်နည်း Channel သို့ဝင်ရန်", url="https://t.me/+G3xrMYI6mQ80MGI1"))
    bot.send_message(message.chat.id, tutorial_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id != ADMIN_CHAT_ID, content_types=['photo', 'text'])
def forward_to_admin(message):
    user_id = message.chat.id
    user_name = message.from_user.username or message.from_user.first_name
    
    if message.content_type == 'photo':
        pack_info = user_states.get(user_id, {}).get("selected_pack", "မရွေးချယ်ရသေးပါ")
        admin_alert = f"🔔 **ငွေလွှဲပြေစာအသစ် ရောက်ရှိလာပါသည်**\n👤 User: {user_name}\n🆔 ID: `{user_id}`\n📦 ပက်ကေ့ချ်: {pack_info}\n\n👇 အရင်ဆုံး အောက်က သက်ဆိုင်ရာခလုတ်ကို နှိပ်ပါ -"
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=f"✅ အတည်ပြုမည် ({pack_info})", callback_data=f"approve_{user_id}_{pack_info}"))
        
        bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=admin_alert, reply_markup=markup, parse_mode="Markdown")
        bot.reply_to(message, "📩 ပြေစာရရှိပါပြီ။ Admin က စစ်ဆေးပြီး ဖိုင်ပို့ပေးပါလိမ့်မည်။")
    
    elif message.content_type == 'text':
        if message.text not in ["🛒 VPN File ဝယ်မည်", "💳 Ngwe Hlwal Rant", "📱 အသုံးပြုရမည့် App", "📖 ဖိုင်ထည့်နည်း", "📞 ဆက်သွယ်ရန်"]:
            pack_info = user_states.get(user_id, {}).get("selected_pack", "မရွေးချယ်ရသေးပါ")
            admin_text = f"💬 **User စာပို့လာပါသည်**\n👤 User: {user_name}\n🆔 ID: `{user_id}`\n📦 ပက်ကေ့ချ်: {pack_info}\n📝 စာသား: {message.text}\n\n👇 အရင်ဆုံး အောက်က သက်ဆိုင်ရာခလုတ်ကို နှိပ်ပါ -"
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=f"✅ အတည်ပြုမည် ({pack_info})", callback_data=f"approve_{user_id}_{pack_info}"))
            
            bot.send_message(ADMIN_CHAT_ID, admin_text, reply_markup=markup, parse_mode="Markdown")
            bot.reply_to(message, "📩 သင့်စာကို အက်ဒမင်ထံ ပေးပို့လိုက်ပါပြီ။")

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID, content_types=['text', 'document'])
def reply_to_user(message):
    global last_active_user
    target_user_id = None
    
    if message.reply_to_message:
        reply_text = message.reply_to_message.caption or message.reply_to_message.text
        if reply_text and "ID:" in reply_text:
            target_user_id = str(int(reply_text.split("ID:")[1].strip().split("\n")[0]))
            
    if not target_user_id and last_active_user:
        target_user_id = last_active_user
        
    if target_user_id:
        try:
            if message.content_type == 'document':
                file_id = message.document.file_id
                file_name = message.document.file_name
                bot.send_document(int(target_user_id), file_id, caption=f"🔑 သင့်အတွက် VPN ဖိုင် ({file_name}) ရောက်ရှိလာပါပြီ ခင်ဗျာ / Fileကို DownLoad Save လိုက်ပါ။")
                bot.reply_to(message, "✅ User ထံ VPN File ပို့ပေးပြီးပါပြီ။")
            elif message.content_type == 'text':
                bot.send_message(int(target_user_id), f"💬 **Admin ထံမှ အကြောင်းပြန်စာ:**\n\n{message.text}")
                bot.reply_to(message, "✅ User ထံ စာသား ပို့ပြီးပါပြီ။")
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {str(e)}")
    else:
        bot.reply_to(message, "💡 ကျေးဇူးပြု၍ Bot ပို့ထားသော စာတွဲကို 'Reply' နှိပ်၍ ဖိုင်ပို့ပေးပါ။")

@bot.message_handler(func=lambda message: message.text == "📞 ဆက်သွယ်ရန်")
def contact_admin(message):
    bot.send_message(message.chat.id, "📞 **ဆက်သွယ်ရန်**\n\nစုံစမ်းမေးမြန်းလိုပါက Admin Telegram အကောင့် @bmt790 သို့ ဆက်သွယ်နိုင်ပါသည်။")

if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.start()
    
    print("Bot စတင်ပွင့်နေပါပြီ...")
    bot.infinity_polling()
