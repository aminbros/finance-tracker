
-- Entry table

CREATE TABLE ft_entry (
  `id` INTEGER primary key,
  `name` char(50),
  `amount` real,
  `weight` real,
  `date` INTEGER,
  `cat` char(50)
);

-- Indexing for Entry table
CREATE INDEX ft_entry_chars ON ft_entry (`name`, `cat`);
CREATE INDEX ft_entry_date ON ft_entry (`date`);

-- Reminder table

CREATE TABLE ft_reminder_entry (
  `id` INTEGER primary key,
  `name` char(50),
  `amount` real,
  `date` INTEGER,
  `cat` char(50)
);

-- Indexing for Reminder Entry table
CREATE INDEX ft_reminder_entry_chars ON ft_entry (`name`, `cat`);
CREATE INDEX ft_reminder_entry_date ON ft_entry (`date`);
