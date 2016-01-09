# Fancyindex

This is a pelican plugin that creates index files of directories based on a custom template.

# Installation

## 1. Clone https://github.com/fleximus/pelican-fancyindex.git and move it into your pelican plugin folder.

## 2. Add these lines to your ```pelicanconf.py```:

<code>
FANCYINDEX_INPUT_PATH = '/path/to/htdocs/'  
FANCYINDEX_OUTPUT_PATH = 'fancyindex'  
FANCYINDEX_SAVE_AS = 'index.html'
</code>

## 3. Do not forget to add fancyindex to your plugin list

```PLUGINS = ['fancyindex']```

## 4. Create a ```fancyindex.html``` template file in ```theme/templates```

## Variables

Variable        | Description
--------------- | --------------------------------------------
fancyindex.root | relative path to ```FANCYINDEX_INPUT_PATH```
file.type       | file type (file / directory)
file.url        | url to the file
file.name       | name of the file or directory
file.size       | file size
file.modified   | modification date

# Known bugs

* ```FANCYINDEX_OUTPUT_PATH``` will be created under the default output path. This might be undesired.
* date formats are not yet configurable

# Disclaimer

This is my first real python code I've ever written. It's likely not to be elegant and/or efficient.
