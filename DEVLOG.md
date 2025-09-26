# Development Log

## Known Issues:

- [ ] EDGAR Client only parses GAAP filings for now, should be extended.
- [ ] EDGAR filing data needs to be normalized by period somehow. Right now, there might be missing quarters in concept data, reducing the meaning and consistency of positions. For example: if `slice[-1]` is a Q3-2025 filing, you cannot reliably expect `slice[-5]` to be Q3-2024. - This can throw off downstream calculations, and enforcing some sort of reliable shape with placeholders, or a new `datetime.date`/fiscal-period based system is needed.


## Log

### Note (2025-06-03) - [@ryan-rashidian](https://github.com/ryan-rashidian):

- This is my first serious project on GitHub. Earlier commits show my learning curve with git, and workflow habits. Since then, I've been refining my process. - Thanks for understanding.

### Note (2025-08-17) - [@ryan-rashidian](https://github.com/ryan-rashidian):

- Though progress has slowed in recent weeks, my intention is to continue development on Qemy into the foreseeable future. This project will continue to be shaped, refined, and refactored as I become a better developer. In the mean time, I'm keeping things simple, focusing on fundamentals, and not digging any deep holes early. I don't want to fall into any perfectionist trap, or constantly change the scope of project goals. - But it may still take a few more months of 'sandbox' testing before anything resembling a user-ended application comes out. 

### Note (2025-09-23) - [@ryan-rashidian](https://github.com/ryan-rashidian):

- The project is settling on a decent structure and conventions. I'm still figuring out the details for implementing plugins, but have a few ideas.

