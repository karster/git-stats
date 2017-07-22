# GIT Stats
Creates useful statistics (activity, author, and keyword) above git repository. Every statistic you can print to console output or to file.

## Activity stats
Creates activity statistics based on time when contributors committed to project repository.

### Usage

```bash
$ cd git-stats
$ python git-activity-stats.py --last-week
```

### Options
`--help` - show help <br />
`--include-merges` - include merge <br />
`--since` <br />
`--until` <br />
`--before` <br />
`--after` <br />
`--last-month` <br />
`--last-week` <br />
`--result` - path to result file <br />

### Output
![activity_stats][activity_stats]

## Author stats
Creates author statistics as commits count, file changed count, count of inserted and deleted code lines etc.

### Usage
```bash
$ cd git-stats
$ python git-author-stats.py --last-week
```

### Options
`--help` - show help <br />
`--include-merges` - include merge <br />
`--since` <br />
`--until` <br />
`--before` <br />
`--after` <br />
`--last-month` <br />
`--last-week` <br />
`--result` - path to result file <br />

### Output
![author_stats][author_stats]

## Keyword stats
Creates keyword statistics based on commit messages. Searchable keywords you can find in `default-keyword.json` file. You can create own json file or use default one.

### Usage
```bash
$ cd git-stats
$ python git-keyword-stats.py --last-week
```

### Options
`--help` - show help <br />
`--include-merges` - include merge <br />
`--since` <br />
`--until` <br />
`--before` <br />
`--after` <br />
`--last-month` <br />
`--last-week` <br />
`--result` - path to result file <br />
`--keywords` - path to keyword JSON file. Default file is `default-keyword.json`

### Output
![keyword_stats][keyword_stats]

## Dependences

- [Texttable](https://pypi.python.org/pypi/texttable)

## Contribution
Have an idea? Found a bug? See [how to contribute][contributing].

## License
MIT see [LICENSE][] for the full license text.

[activity_stats]: docs/activity_stats.png
[author_stats]: docs/author_stats.png
[keyword_stats]: docs/keyword_stats.png

[license]: LICENSE.md
[contributing]: CONTRIBUTING.md