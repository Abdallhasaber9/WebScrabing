{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "xgFZ7BuIJLz6",
        "outputId": "5efcaf48-c78e-4a71-94a5-193bfc916d3d"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            " Enter job title to search on Wuzzuf: business inteligence\n",
            " Scraping page 1 of 8...\n",
            " Scraping page 2 of 8...\n",
            " Scraping page 3 of 8...\n",
            " Scraping page 4 of 8...\n",
            " Scraping page 5 of 8...\n",
            " Scraping page 6 of 8...\n",
            " Scraping page 7 of 8...\n",
            " Scraping page 8 of 8...\n",
            "\n",
            " Job Results (All):\n"
          ]
        }
      ],
      "source": [
        "import requests\n",
        "from bs4 import BeautifulSoup\n",
        "import pandas as pd\n",
        "import math\n",
        "\n",
        "try:\n",
        "    from google.colab import data_table\n",
        "    data_table.enable_dataframe_formatter()\n",
        "    USE_COLAB = True\n",
        "except:\n",
        "    USE_COLAB = False\n",
        "\n",
        "def find_no_of_jobs(job):\n",
        "    req = requests.get('https://wuzzuf.net/search/jobs/?a=hpb&q=' + job.replace(' ', '%20'))\n",
        "    soup = BeautifulSoup(req.content, 'lxml')\n",
        "    jobs_tag = soup.find('strong')\n",
        "    jobs = int(jobs_tag.text.replace(',', '')) if jobs_tag else 0\n",
        "    pages = math.ceil(jobs / 15)\n",
        "    return jobs, pages\n",
        "\n",
        "def scrap_pages(query):\n",
        "    num_jobs, num_pages = find_no_of_jobs(query)\n",
        "    query_url = query.replace(' ', '%20')\n",
        "\n",
        "    titles_lst, links_lst, occupations_lst, companies_lst, specs_lst = [], [], [], [], []\n",
        "    location_lst, company_address_lst = [], []\n",
        "\n",
        "    for pageNo in range(num_pages):\n",
        "        print(f\" Scraping page {pageNo + 1} of {num_pages}...\")\n",
        "        url = f'https://wuzzuf.net/search/jobs/?a=hpb&q={query_url}&start={pageNo * 15}'\n",
        "        page = requests.get(url)\n",
        "        soup = BeautifulSoup(page.content, 'lxml')\n",
        "\n",
        "        jobs = soup.find_all(\"div\", {'class': 'css-pkv5jc'})\n",
        "\n",
        "        for job in jobs:\n",
        "            title_tag = job.find(\"h2\", {'class': 'css-m604qf'})\n",
        "            titles_lst.append(title_tag.a.text.strip() if title_tag and title_tag.a else '')\n",
        "            links_lst.append('https://wuzzuf.net' + title_tag.a['href'] if title_tag and title_tag.a else '')\n",
        "\n",
        "            occ_tag = job.find(\"div\", {'class': 'css-1lh32fc'})\n",
        "            occupations_lst.append(occ_tag.text.strip() if occ_tag else '')\n",
        "\n",
        "            company_tag = job.find(\"a\", {'class': 'css-17s97q8'})\n",
        "            companies_lst.append(company_tag.text.strip() if company_tag else '')\n",
        "\n",
        "            company_info = job.find(\"div\", {'class': 'css-d7j1kk'})\n",
        "            if company_info:\n",
        "                spans = company_info.find_all('span', {'class': 'css-5wys0k'})\n",
        "                company_address_lst.append(spans[0].text.strip() if spans else '')\n",
        "            else:\n",
        "                company_address_lst.append('')\n",
        "\n",
        "            specs_tag = job.find(\"div\", {'class': 'css-y4udm8'})\n",
        "            specs_lst.append(specs_tag.text.strip() if specs_tag else '')\n",
        "\n",
        "            location_tag = job.find(\"span\", {'class': 'css-5wys0k'})\n",
        "            location_lst.append(location_tag.text.strip() if location_tag else '')\n",
        "\n",
        "    scraped_data = {\n",
        "        'Title': titles_lst,\n",
        "        'Link': links_lst,\n",
        "        'Occupation': occupations_lst,\n",
        "        'Company': companies_lst,\n",
        "        'Specs': specs_lst,\n",
        "        'Location': location_lst,\n",
        "        'Company Address': company_address_lst\n",
        "    }\n",
        "\n",
        "    df = pd.DataFrame(scraped_data)\n",
        "    return scraped_data, df\n",
        "\n",
        "\n",
        "job = input(\" Enter job title to search on Wuzzuf: \")\n",
        "data, df = scrap_pages(job)\n",
        "\n",
        "print(\"\\n Job Results (All):\")\n",
        "if USE_COLAB:\n",
        "    data_table.DataTable(df)\n",
        "else:\n",
        "    print(df.to_string(index=False))\n",
        "\n",
        "\n",
        "df.to_csv(f\"{job.replace(' ', '_')}_wuzzuf_jobs.csv\", index=False)\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "job = input(\" Enter job title to search on Wuzzuf: \")\n",
        "data, df = scrap_pages(job)\n",
        "\n",
        "print(\"\\n Job Results Table:\")\n",
        "\n",
        "if USE_COLAB:\n",
        "    from google.colab import data_table\n",
        "    data_table.DataTable(df)\n",
        "else:\n",
        "    print(df.to_string(index=False))\n",
        "\n",
        "\n",
        "csv_file = f\"{job.replace(' ', '_')}_wuzzuf_jobs.csv\"\n",
        "df.to_csv(csv_file, index=False)\n",
        "print(f\"\\n Saved to: {csv_file}\")\n",
        "\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "HzCLmMpuPJyw",
        "outputId": "8d119198-7355-450a-bf7b-07694bdc3146"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            " Enter job title to search on Wuzzuf: business inteligence\n",
            " Scraping page 1 of 8...\n",
            " Scraping page 2 of 8...\n",
            " Scraping page 3 of 8...\n",
            " Scraping page 4 of 8...\n",
            " Scraping page 5 of 8...\n",
            " Scraping page 6 of 8...\n",
            " Scraping page 7 of 8...\n",
            " Scraping page 8 of 8...\n",
            "\n",
            " Job Results Table:\n",
            "\n",
            " Saved to: business_inteligence_wuzzuf_jobs.csv\n"
          ]
        }
      ]
    }
  ]
}