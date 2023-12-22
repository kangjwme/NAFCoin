import discord
from discord.ext import commands
import time
import point_ext
import random
import uuid

bot = discord.Bot()

@bot.event
async def on_ready(): 
    print("機器人已啟動")

@bot.slash_command(name="add增加點數",description="增加用戶 NAF Coin 數量")
async def add(ctx, id: discord.Option(str, "增加對象ID",require = True), point: discord.Option(int, "增加 NAF Coin 數量",require = True)):
    if ctx.author.id != 1095770087966916731:
        await ctx.respond("你沒有使用的權限", ephemeral=True)
        return
    await point_ext.add_point(id, point)
    await ctx.respond(f"增加 {id} {point} 枚 NAF Coin", ephemeral=True)

@bot.slash_command(name="sub減少點數",description="減少用戶 NAF Coin 數量")
async def sub(ctx, id: discord.Option(str, "減少對象ID",require = True), point: discord.Option(int, "減少 NAF Coin 數量",require = True)):
    if ctx.author.id != 1095770087966916731:
        await ctx.respond("你沒有使用的權限", ephemeral=True)
        return
    await point_ext.sub_point(id, point)
    await ctx.respond(f"減少 {id} {point} 枚 NAF Coin", ephemeral=True)
    
    
@bot.slash_command(name="set設定點數",description="設定用戶 NAF Coin 數量")
async def set(ctx, id: discord.Option(str, "設定對象ID",require = True), point: discord.Option(int, "設定 NAF Coin 數量",require = True)):
    if ctx.author.id != 1095770087966916731:
        await ctx.respond("你沒有使用的權限", ephemeral=True)
        return
    await point_ext.set_point(id, point)
    await ctx.respond(f"設定 {id} {point} 枚 NAF Coin", ephemeral=True)

@bot.slash_command(name="addcode增加兌換碼",description="增加指定獎品兌換碼")
async def addcode(ctx, id: discord.Option(int, "增加兌換碼獎品ID",require = True), code: discord.Option(str, "增加兌換碼",require = True)):
    if ctx.author.id != 1095770087966916731:
        await ctx.respond("你沒有使用的權限", ephemeral=True)
        return
    await point_ext.add_reward_code(id, code)
    await ctx.respond(f"增加 {id} {code} 兌換碼", ephemeral=True)

@bot.slash_command(name="listredeem列出獎項格式",description="列出資料庫")
async def listredeem(ctx):
    if ctx.author.id != 1095770087966916731:
        await ctx.respond("你沒有使用的權限", ephemeral=True)
        return
    data = await point_ext.get_reward()
    await ctx.respond(f"```\n{data}\n```", ephemeral=True)
bot.run(TOKEN)