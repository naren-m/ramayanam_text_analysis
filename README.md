# Cli for reading ramayanam

## Folder structure
```
-RamyanaSlokas
|
|
-- kanda name
    |
    |
    -- Sarga-sloka file contains all slokas fo that sarga
    -- Sarga-meaning file contains all meanings fo that sarga
    -- Sarga-translation file contains all translations fo that sarga
<<<<<<< HEAD

## Ramayana Commentaries Downloader

This project now includes a script to download Sanskrit commentaries from the Valmiki Ramayana website ([https://www.valmiki.iitk.ac.in](https://www.valmiki.iitk.ac.in)).

### Prerequisites for the Commentary Downloader

- Python 3.6 or higher
- Required Python packages (added to requirements.txt):
  - requests
  - beautifulsoup4
  - tqdm

### Usage of the Commentary Downloader

#### Basic Usage

To download all commentaries sequentially:

```bash
python fetch_ramayana_commentaries.py
```

#### Resume an Interrupted Download

If the download process was interrupted, you can resume from where it left off:

```bash
python fetch_ramayana_commentaries.py --resume
```

#### Parallel Downloading

To speed up the download process, you can use multiple threads:

```bash
python fetch_ramayana_commentaries.py --parallel 4
```

### Output Structure

The commentaries are organized in the following structure:

```text
./output/
  Bhusana/
    kanda_1/
      sarga_1.html
      sarga_2.html
      …
  Kataka/
    kanda_1/
      sarga_1.html
      …
  commentaries_index.json
```

The `commentaries_index.json` file contains metadata about each downloaded commentary, including:

- Commentary ID and name
- Kanda and Sarga numbers
- Absolute file path
- Download timestamp
=======
```
>>>>>>> 42e65c54b8ab9ac902edfb707cda2602821a97fe
