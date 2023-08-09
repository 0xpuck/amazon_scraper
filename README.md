# Amazon UK Scrapy Spider

This repository contains a Scrapy spider designed to scrape product information from Amazon UK based on provided search terms, categories, and filters.

## Features

- Search products by term and category on Amazon UK.
- Filter results by a keyword. For example, you can search for "Intel NUC" in the "computers" category and filter the results by "i7". One keyword per search is supported for now. 
- Exclude sponsored product links.
- Pagination support to scrape multiple pages of search results.
- **Deduplication Filter**: Ensures that the output contains only unique product listings. This feature effectively makes the **'exclude_sponsored'** parameter deprecated, as the deduplication filter will inherently remove multiple occurrences of the same sponsored links.
- Save results to a CSV file.

## Setup and Installation

1. **Clone the Repository**:
```bash
git clone https://github.com/loglux/Amazon_UK.git
cd Amazon_UK/amazon_uk
```

2. **Set Up a Virtual Environment**:
```bash
python3 -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate.bat instead
``` 

3. **Install Dependencies**:
 ```bash
pip install scrapy
````

4. **Run the Spider**:
```bash
scrapy crawl amazon_uk -a search_term="iphone" -a category="electronics" -a filter="apple" -a exclude_sponsored="True" -o iphone.csv
```

## Parameters

- `search`: The search term you want to use (e.g., "Intel NUC").
- `category`: The category within which to search (e.g., "computers").
- `filter_word`: An optional parameter to further filter search results by a specific keyword.
- `exclude_sponsored`: An optional parameter to exclude sponsored product links from the results. Set to "True" to exclude sponsored links.

## Deduplication Filter
To ensure the quality of the scraped data, a deduplication filter is implemented in the Scrapy pipeline. This filter automatically removes any products that have identical or very similar URLs, ensuring that the output contains only unique product listings.

## How it Works
The Scrapy Spider collects product URLs while crawling through the Amazon UK product listings. Before finalizing the scraped data, the pipeline checks each product URL for similarity. If a duplicate or very similar URL is found, that product entry is excluded from the output.

## Usage
The deduplication filter is automatically applied whenever you run the Scrapy spider. Just use the standard command as shown above.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

