OWNERID=802199418345357353
########^^^your id here^^^
from nextcord import Intents
from nextcord.ext import commands
import json
intents=Intents.default()
intents.message_content = True
bot=commands.Bot(command_prefix='$', intents=intents)
def todos_get():
    with open("todos.json", "r") as f:
        return json.loads(f.read())
def todos_update(j):
    with open("todos.json", "w") as f:
        return f.write(json.dumps(j))
@bot.command(description="add new todo for Eldyj")
async def todo(e):
    todos = todos_get()
    todo = {
        'author'   : e.author.name + "#" + e.author.discriminator,
        'title'    : e.message.content[5:].strip().split()[0],
        'content'  : ' '.join(e.message.content[5:].strip().split()[1:]),
        'completed': False
    }
    print(todo['content'])
    if todo['content'] == "":
        await e.reply("you can't add ampty todo")
        return
    await e.reply(f"todo `{todo['title']}[{len(todos)}]` added succesfully")
    todos.append(todo)
    todos_update(todos)
@bot.command(description="show all todos")
async def all(e):
  await e.reply(''.join([f"`{i[1]['title']}@{i[1]['author']}[{i[0]}]`({':white_check_mark:' if i[1]['completed'] else ':negative_squared_cross_mark:'}):\n  {i[1]['content']}\n" for i in enumerate(todos_get())]) or "empty")
@bot.command(description="show completed todos")
async def completed(e):
  await e.reply(''.join([f"`{i[1]['title']}@{i[1]['author']}[{i[0]}]`(:white_check_mark:):\n  {i[1]['content']}\n" for i in enumerate(todos_get()) if i[1]['completed']]) or "empty")
@bot.command(description="show uncompeted todos")
async def uncompleted(e):
  await e.reply(''.join([f"`{i[1]['title']}@{i[1]['author']}[{i[0]}]`(:negative_squared_cross_mark:):\n  {i[1]['content']}\n" for i in enumerate(todos_get()) if not i[1]['completed']]) or "empty")
@bot.command(description="remove todo")
async def rm(e):
  if e.message.author.id!=OWNERID:
    e.reply("err: you haven't permission to do that")
    return
  try:
    index=int(e.message.content[4:])
  except:
    await e.reply("err: non numeric index")
    return
  todos=todos_get()
  if index>=len(todos):
    await e.reply("err: index out of bounds")
    return
  todos.pop(index)
  todos_update(todos)
  await e.reply(f"todo [{index}] removed succesfully")
@bot.command(description="change todo state")
async def change(e):
  if e.message.author.id!=OWNERID:
    e.reply("err: you haven't permission to do that")
    return
  try:
    index=int(e.message.content[8:])
  except:
    await e.reply("err: non numeric index")
    return
  todos=todos_get()
  if index>=len(todos):
    await e.reply("err: index out of bouds")
    return
  todos[index]['completed']=not todos[index]['completed']
  todos_update(todos)
  await e.reply(f"task [{index}] changed succesfully")
@bot.command(description="reset todos")
async def reset(e):
  if e.message.author.id!=OWNERID:
    e.reply("err: you haven't permission to do that")
    return
  todos_update([])
  await e.reply("todos reseted succesfully")
with open("token.txt","r") as f:
  bot.run(f.read())
