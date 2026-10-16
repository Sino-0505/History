import os, sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
TOKEN=os.environ.get("BOT_TOKEN")
conn=sqlite3.connect("base.db", check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS coefs (coef REAL, time TEXT, hour INTEGER)")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ @Sino0505_bot 24/7 фурӯзон!\n/live\n/history\n/add 2.5")
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        c=float(context.args[0]); now=datetime.now()
        conn.execute("INSERT INTO coefs VALUES (?,?,?)",(c,now.strftime("%H:%M:%S"),now.hour)); conn.commit()
        await update.message.reply_text(f"Нигоҳ доштам: {c}x")
    except: await update.message.reply_text("/add 2.34")
async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cur=conn.execute("SELECT coef,time FROM coefs ORDER BY rowid DESC LIMIT 10").fetchall()
    if not cur: await update.message.reply_text("Холӣ"); return
    t="🚀 Охирин 10:\n"
    for a,b in cur: t+=f"{a}x - {b}\n"
    await update.message.reply_text(t)
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cur=conn.execute("SELECT hour,COUNT(*),AVG(coef) FROM coefs GROUP BY hour").fetchall()
    if not cur: await update.message.reply_text("Нест"); return
    t="📊 Ба соатҳо:\n"
    for h,c,a in cur: t+=f"{h}:00 - {c} дона, миёна {a:.2f}x\n"
    await update.message.reply_text(t)
app=ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("live", live))
app.add_handler(CommandHandler("history", history))
app.run_polling()
