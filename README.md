# SongSeeker Card Generator

## Introduction
The SongSeeker Card Generator is a Python script designed to create visual cards based on song data. This tool is part of the [SongSeeker project](https://github.com/andygruber/songseeker), a music guessing game.

## Features
- Generate visual cards for songs.
- PDF output.
- Input data in CSV format.

## Prerequisites
Before you start using the SongSeeker Card Generator, make sure you have Python installed on your system. The script is tested with Python 3.11 and above. You can download and install Python from [here](https://www.python.org/downloads/).

## Installation
Clone the repository to your local machine using the following command:
```bash
git clone https://github.com/andygruber/songseeker-card-generator.git
```
Navigate to the cloned directory:
```bash
cd songseeker-card-generator
```
Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

To run the script, use the following command:

```bash
python card_generator.py <input_csv_path> <output_pdf_path>
```

### Example

```bash
python card_generator.py data/example-youtube-songs.csv example.pdf
```

You can also add an icon to the card by using the `--icon` flag:
```bash
# Add icon from a url
python card_generator.py data/example-youtube-songs.csv example.pdf --icon https://github.com/andygruber/songseeker/blob/main/icons/icon-96x96.png?raw=true
# Add icon from a local file
python card_generator.py data/example-youtube-songs.csv example.pdf --icon ../songseeker/icons/icon-96x96.png
```


## CSV Input Format

The input CSV file should have the following format:

*   `Title`: The title of the song.
*   `Artist`: The artist of the song.
*   `Year`: The release year of the song.
*   `URL`: The YouTube URL of the song. If the song does not start at the beginning of the video, you may also add the starting time in seconds to the end of the link, like `?t=16`.
*   `backcol`: (optional) background color of the card

Make sure your CSV file includes headers and the data is separated by commas.

An example can be found in `data/example-youtube-songs.csv`.

## Contributing

Contributions to the SongSeeker Card Generator are welcome. Please ensure to update tests as appropriate.

## License

This project is licensed under the AGPL-3.0 license - see the LICENSE file for details.