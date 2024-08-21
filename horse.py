import disnake, random
from disnake.ext import commands
@bot.slash_command(name="경마", description="경마 도박을 하여 돈을 얻거나 잃습니다.")
async def 경마(interaction: disnake.ApplicationCommandInteraction, 금액: int = commands.Param(description="베팅할 금액"), 말 = commands.Param(choices=["말1", "말2", "말3", "말4"], description="선택할 말")):
    balance = get_balance("game", interaction.author.id)
    if balance is None:
        await interaction.response.send_message(embed=embeds("게임 오류", "/게임등록 명령어를 사용해 계정을 등록하세요!"))
        return
    
    if 금액 <= 1000:
        await interaction.response.send_message(embed=embeds("오류", "1000원 이상의 금액을 입력해주세요."))
        return
    
    if 금액 > balance:
        await interaction.response.send_message(embed=embeds("오류", "잔액이 부족합니다."))
        return

    horses = ["말1", "말2", "말3", "말4"]
    horse_emoji = "🏇"
    finish_line = 20 

    chosen_horse = f"말{말[-1]}"

    embed = disnake.Embed(title="경마 도박", description=f"{interaction.author.mention}님, {horse_emoji} {chosen_horse}를 선택하셨습니다!\n경주가 곧 시작됩니다!", color=0xb1b9c4)
    await interaction.response.send_message(embed=embed)
    message = await interaction.original_message()
    
    race_progress = {horse: 0 for horse in horses}

    while all(progress < finish_line for progress in race_progress.values()):
        race_progress = {horse: progress + random.randint(1, 3) for horse, progress in race_progress.items()}
        race_status = "\n".join([f"{horse_emoji} {horse}: {'━' * progress}{horse_emoji}{'━' * (finish_line - progress)}🏁" for horse, progress in race_progress.items()])
        embed.description = f"🏇 경주 진행상황:\n{race_status}"
        await message.edit(embed=embed)
        await asyncio.sleep(1)

    winner_horse = max(race_progress, key=race_progress.get)
    result_message = f"경주 결과: {horse_emoji} {winner_horse}이(가) 우승했습니다!"
    
    if chosen_horse == winner_horse:
        winnings = 금액 * 5
        update_balance("game", interaction.author.id, winnings)
        result_embed = embeds("경마 결과", f"{interaction.author.mention}님, {horse_emoji} {chosen_horse}를 선택하여 {winnings}원을 얻었습니다!\n현재 잔액: {balance + winnings}원\n{result_message}")
    else:
        update_balance("game", interaction.author.id, -금액)
        result_embed = embeds("경마 결과", f"{interaction.author.mention}님, {horse_emoji} {chosen_horse}를 선택하여 {금액}원을 잃었습니다.\n현재 잔액: {balance - 금액}원\n{result_message}")
    
    await message.edit(embed=result_embed)
