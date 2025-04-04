from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

referral_count = {}

async def new_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        adder_id = update.message.from_user.id
        adder_name = update.message.from_user.full_name
        count = len(update.message.new_chat_members)

        if adder_id in referral_count:
            referral_count[adder_id]["count"] += count
        else:
            referral_count[adder_id] = {
                "name": adder_name,
                "count": count
            }

        await update.message.reply_text(
            f"{adder_name} {count} ta odam qo‘shdi."
        )

async def stat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not referral_count:
        await update.message.reply_text("Hali hech kim odam qo‘shmagan.")
        return

    sorted_users = sorted(referral_count.items(), key=lambda x: x[1]['count'], reverse=True)
    text = "Statistika:\n\n"
    for i, (user_id, data) in enumerate(sorted_users, 1):
        text += f"{i}. {data['name']}: {data['count']} ta odam\n"

    await update.message.reply_text(text)

async def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()  # Bu yerga tokenni joylang

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_handler))
    app.add_handler(CommandHandler("stat", stat_command))

    print("Bot ishga tushdi!")
    await app.run_polling()

import asyncio
asyncio.run(main())
