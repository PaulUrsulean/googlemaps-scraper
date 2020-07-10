# -*- coding: utf-8 -*-
from googlemaps import GoogleMapsScraper
from datetime import datetime, timedelta
import argparse
import pandas as pd

HEADER = ['id_review', 'caption', 'rating', 'username', 'url_user']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=100, help='Number of reviews to scrape')
    parser.add_argument('--i', type=str, default='urls.txt', help='target URLs file')
    parser.add_argument('--place', dest='place', action='store_true', help='Scrape place metadata')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Run scraper using browser graphical interface')
    parser.add_argument('--csv-path', type=str, default='data/gm_reviews.csv', help='target CSV file')
    parser.set_defaults(place=False, debug=False, source=False)

    args = parser.parse_args()

    df = pd.DataFrame(columns=HEADER)
    
    try:

        with GoogleMapsScraper(debug=args.debug) as scraper:
            with open(args.i, 'r') as urls_file:
                for url in urls_file:

                    if args.place:
                        print(scraper.get_account(url))
                    else:
                        error = scraper.sort_by_date(url)
                        if error == 0:

                            n = 0
                            pbar = tqdm(desc="Fetching reviews")
                            while n < args.N:
                                reviews = scraper.get_reviews(n)

                                for r in reviews:
                                    df=df.append(r, ignore_index=True)

                                n += len(reviews)
                                pbar.update(len(reviews))
                                
                            pbar.close()
                                
    except:
        if len(df) > 0: print("Error encountered, dumping partial csv: {}".format(df.to_csv()))
        raise
    
    df.to_csv(args.csv_path)
