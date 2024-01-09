# VillaVenture

Welcome to VillaVenture, the perfect scraper for the amazingly old and dogshit of a site - bgvakancia!

## Features

- Filter villas based on minimum and maximum capacity.
- Compile a list of suitable villas into a CSV file with detailed information including title, capacity, description, price, and location.

## How to Use

To use VillaVenture Party Picks, follow these steps:

1. Ensure you have Python installed on your system.
2. Install the required Python packages using `pip install requests beautifulsoup4`.
3. Clone this repository to your local machine.
4. Run the script with your desired parameters:
    ```shell
    python3 villa_venture.py --min_capacity 20 --max_capacity 40 --date "DD.MM.YYYY"
    ```
    Replace `--min_capacity` and `--max_capacity` with the minimum and maximum number of guests. Replace `--date` with your event date in "DD.MM.YYYY" format.
5. Once the script finishes, you will find a CSV file named `villas_info_DD-MM_HH-MM.csv` in the script directory. This file contains all the details of the villas that match your criteria.

## Contributing

We welcome contributions to VillaVenture, Simono! If you have suggestions for improvements or bug fixes, please open an issue or a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
