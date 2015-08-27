# Configure
make a copy of config.example.json file and change database file 
name if you like.

You can add `bin` directory in PATH variable to be able to run program easier.

# Start tracking 

```
# set the default category
ft env set cat food
#  add <name>  <amount> [<weight>] [<cat>]
ft add apple -1.2 2.0
ft add almond -5 0.5
ft add coffee -1

# taxi
ft add taxi -4 --cat trans

ft add webdev 500 --cat dev

```

# Edit data as you wish

```

ft list food

# find the id of entry you want to edit
# Currently it is the last number

ft edit <id> --name correct-name --amount -1
ft delete <id>

```

# Track Balance

```

ft balance taxi

ft balance cat food

```

# Reminder


Reminder helps you remember how much you owe or they owe you. For example look
at the following.

```
# You can omit category
ft env unset cat

# take some money from robert
ft add robert -500

# later return 200
ft add reminder robert 200
# and another 50
ft add reminder robert 50

# after awhile you can see the balance in reminder
ft balance reminder robert
# and return is -250

```

That's it.
