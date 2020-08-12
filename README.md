Installation:

    pip3 install flit
    flit install --symlink --python $(which python3)

It should install to `~/.local/bin`, which you might have to add to your path

Usage:

- Remove leading dashes and spaces:
  `regexrename '^[- ]' '' *`

- Change specific words in filenames:
  `regexrename Foo Bar *.mp3`

- Preview changes:
  `regexrename -n 'Monkey*' Ape Monkeyyyy`

- Use parenthesized numbers to resolve conflicts:
  `regexrename -c Monkeyy* Ape Monkey Monkeyy Monkeyyy`
  Would result in Ape, Ape (1), and Ape (2)
