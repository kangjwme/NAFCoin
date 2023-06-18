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

@bot.slash_command(name="sign每日簽到",description="每日簽到，獲得 NAF Coin 1 ~ 15 枚")
@commands.guild_only()
async def sign(ctx):
    if ctx.author.bot:
        await ctx.respond("你衝三小簽到？", ephemeral=True)
        return
    if(await point_ext.is_timestamp_30_days_apart(ctx.author.created_at.timestamp())):
        # 確認帳號有滿 30 天
        point = max(1, min(int(random.gauss(8.5, 3)), 15))
        response = await point_ext.sign(ctx.author.id, point)
        if response[0] == 1:
            await ctx.respond(f"<:I_Love_NAFStore:1096042862199713885> 簽到完成，你已獲得 `{point}` 枚 NAF Coin， <t:{response[1]}> 後記得再來簽到唷！")
            await point_ext.point_log(ctx.author.id,"每日簽到",point)
        else:
            await ctx.respond(f"<a:xo_cross:1096042864858902708> 您今日已經簽到過了，<t:{response[1]}> 後再來簽到吧！", ephemeral=True)
        return
    else:
        await ctx.respond("<a:xo_cross:1096042864858902708> 您的帳號創建時間不足30天，無法簽到！", ephemeral=True)
        return

@bot.slash_command(name="give點數轉贈",description="轉贈 NAF Coin 給其他人")
@commands.guild_only()
async def give(ctx, member: discord.Option(discord.Member, "轉贈對象",required = True), point: discord.Option(int, "轉贈 NAF Coin 數量(最少 300 枚)",required = True,min_value = 300)):
    if member.bot:
        await ctx.respond("<a:xo_cross:1096042864858902708> 你送給機器人衝三小？", ephemeral=True)
        return
    if ctx == member:
        await ctx.respond("<a:xo_cross:1096042864858902708> 你送給自己衝三小？", ephemeral=True)
        return
    send_user_point = await point_ext.check_point(ctx.author.id)
    if send_user_point < int(point*1.05):
        await ctx.respond(f"您的 NAF Coin 不足，本次轉帳含手續費需要 {int(point*1.05)} 枚 NAF Coin，無法轉贈！", ephemeral=True)
        return
    await point_ext.sub_point(ctx.author.id, int(point*1.05))
    await point_ext.add_point(member.id, point)
    await point_ext.point_log(ctx.author.id,f"轉帳出去給{member.id}",point)
    await point_ext.point_log(member.id,f"從{ctx.author.id}收到轉帳",point)
    await ctx.respond(f"<a:check:1096042843174342738> 轉帳完成", ephemeral=True)

@bot.slash_command(name="point查詢點數",description="查自己（或別人）的 NAF Coin 點數")
@commands.guild_only()
async def give(ctx, search_member: discord.Option(discord.Member, "查詢對象（留空=自己）",required = False)):
    if search_member == None:
        search_member = ctx.author
    point = await point_ext.check_point(search_member.id)
    await ctx.respond(f"{search_member.mention} 有 {point} 枚 NAF Coin", ephemeral=True)

@bot.slash_command(name="top前十排行榜",description="列出前十名 NAF Coin 持有者")
@commands.guild_only()
async def top(ctx):
    rawpoint_data = await point_ext.get_rawpoint_data()
    sorted_ids = sorted(rawpoint_data.keys(), key=lambda x: rawpoint_data[x]['point'], reverse=True)
    top_10_ids = sorted_ids[:10]
    top = f"目前總發行 NAF Coin 數量：__{await point_ext.total_point()}__ 枚，總參與人數：__{await point_ext.total_user()}__ 人\n\n"
    for i, id in enumerate(top_10_ids):
        top += f"第 {i+1} 名｜<@!{id}> ({rawpoint_data[id]['point']} 枚)\n"
    await ctx.respond(top, ephemeral=True)

@bot.slash_command(name="redeem兌換商品",description="把 NAF Coin 換成喜歡的形狀！")
@commands.guild_only()
async def redeem(ctx, id: discord.Option(int, "商品序號(留空可查詢現可兌換商品)",required = False)):
    data = await point_ext.get_reward()
    if id != None:
        if id > len(data['reward']) or id < 1:
            await ctx.respond(f"<a:xo_cross:1096042864858902708> 商品序號輸入錯誤，請輸入 1 ~ {len(data['reward'])} 的正整數", ephemeral=True)
            return
        # 檢查是否有庫存
        if data['reward'][id-1]['stock'] == 0:
            await ctx.respond(f"<a:xo_cross:1096042864858902708> 「{data['reward'][id-1]['display_name']}」已經兌換完畢，請選擇其他商品", ephemeral=True)
            return
        # 檢查是否有足夠的 NAF Coin
        if await point_ext.check_point(ctx.author.id) < data['reward'][id-1]['price']:
            await ctx.respond(f"<a:xo_cross:1096042864858902708> 您未有足夠的 NAF Coin，「{data['reward'][id-1]['display_name']}」 需要 {data['reward'][id-1]['price']} 枚", ephemeral=True)
            return
        # 兌換給使用者
        code = await point_ext.pop_reward_code(id)
        await point_ext.sub_point(ctx.author.id, data['reward'][id-1]['price'])
        await point_ext.point_log(ctx.author.id,f"兌換{data['reward'][id-1]['display_name']}，兌換代碼：{code}",data['reward'][id-1]['price'])
        await ctx.respond(f"<a:check:1096042843174342738> 兌換「{data['reward'][id-1]['display_name']}」成功，請查收您的兌換碼：`{code}`，並妥善保存，消失不得要求補發\n\n兌換說明：\n> {data['reward'][id-1]['description']}", ephemeral=True)
        return
    reply = "目前可兌換商品：\n"
    for i in data['reward']:
        reply += f"{i['id']}. `{i['price']:5}`枚、庫存 `{i['stock']:02d}`：**{i['display_name']}**\n"
    await ctx.respond(reply, ephemeral=True)

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.respond("<a:xo_cross:1096042864858902708> 很抱歉，我們不回應私訊！")
        return
    else:
        code = uuid.uuid4()
        await point_ext.error_log(ctx, error, code)
        await ctx.respond(f"<a:xo_cross:1096042864858902708> 請將此錯誤代碼回報給 https://discord.gg/nafstore 專門負責的頻道：`{code}`", ephemeral=True)

bot.run("這邊是酷酷的TOKEN")
