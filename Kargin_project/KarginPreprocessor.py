# Date written 19.05.21
# you need to run 3 lines below at least once
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer


class KarginPreprocessor:
    """Class implements all the necessary functions for preprocessing the text
    
    list of funcs: |br|
    1. make_lowercase |br|
    2. remove_stopwords |br|
    3. remove_extra_spaces |br|
    4. remove_punctuations_and_symbols |br|
    5. remove_digits |br|
    6. standardize_metrics |br|
    7. lemmatize |br|
    8. pipeline |br|

    Note:
        expects nltk library to be imported

    .. |br| raw:: html

      <br>
    """
    def __init__(self, text, methods=['make_lowercase', 'remove_stopwords', \
                                      'remove_extra_spaces', 'remove_punctuations_and_symbols', \
                                      'standardize_metrics', 'remove_digits', 'lemmatize']):
        """
        Args:
            text (str): text to preprocesed
            methods (:obj:`list` of :obj:`str`): list of functions to execute in ``pipeline()``
        """
        self.text = text
        self.methods = methods
        
    def make_lowercase(self, text=None):
        """Function takes as input a string and converts all the letters to
        lowercase
        
        Note:
            function also update the class variable ``text``

        Examples:
            >>> print(make_lowercase('THIs iS soMe 123123'))
            this is some 123123

        Args:
            text (str) : text to make lowercase
        
        Returns:
            str: text converted to lowercase
        """
        if text is None:
            text = self.text

        self.text = text.lower()
        return text.lower()

    def remove_stopwords(self, text=None, stopwords=stopwords.words('english')):
        """Function takes as input list of words and removes it from the text

        Note:
            function also updates the class variable ``text``
        
        Examples:
            >>> print(remove_stopwords('i remember what i havent forgotten'))
            remember havent forgotten

        Args:
            text (str) : text to remove stopwords from defaults to self.text
            stopwords (:obj:`list` of :obj:`str`): list of words to remove from text
            defaults to nltk's list

        Returns:
            str: text without stopwords
        """
        if text is None:
            text = self.text

        word_tokens = word_tokenize(text) 
        filtered_words = [w for w in word_tokens if w not in stopwords] 
        filtered_text = " ".join(filtered_words)
        
        self.text = filtered_text
        return filtered_text  

    def remove_extra_spaces(self, text=None):
        """Function removes all the unnecessary spaces between words

        Note:
            function also update the class variable ``text``

        Examples:
            >>> print(remove_extra_spaces('Hello    Finnowciqic'))
            Hello Finnowciqic

        Args:
            text (str) : text to remove extra spaces from
        
        Returns:
            str:  text without extra spaces
        """
        if text is None:
            text = self.text

        self.text = re.sub(r'\s+', ' ', text)
        return self.text

    def remove_punctuations_and_symbols(self, text=None):
        """Function removes all the punctuation and special characterts

        Note:
            function also update the class variable ``text``

        Examples:
            >>> print(remove_punctuations_and_symbols('$#! asdas, , 888323'))
            asdas 888323

        Args:
            text (str) : text to preprocess
        
        Returns:
            str:  text without special symbols and punctuation
        """
        if text is None:
            text = self.text

        self.text = re.sub('\W+',' ', text)
        return self.text

    def remove_digits(self, text=None):
        """Function removes all the digits from text

        Note:
            function also update the class variable ``text``
            If the digit is next to word it won't get removed

        Examples:
            >>> print(remove_digits('this is a number 509'))
            This is a number
            >>> print(remove_digits('number 509 and num 123v'))
            number and num 123v

        Args:
            text (str) : text to preprocess
        
        Returns:
            str:  text without digits
        """
        if text is None:
            text = self.text

        self.text = " ".join([w for w in text.split() if not w.isdigit()])
        return self.text

    def standardize_metrics(self, text=None):
        """Function converts all the metrics to standard form.

        Note:
            function also update the class variable ``text``

        Examples:
            >>> print(standardize_metrics('Bulb is 220v'))
            Bulb is metricV

        Args:
            text (str) : text to preprocess
        
        Returns:
            str:  text with all the metrics brough to standard form
        """
        if text is None:
            text = self.text

        text = re.sub(r'\b[\d\.\/]+\s?(v|volt)\b', 'metricV', text)
        text = re.sub(r'\b[\d\.\/]+\s?(amp|amps|ampere|amperes)\b', 'metricA', text)
        text = re.sub(r'\b[\d\.\/]+\s?(mah|ah|ampere-hour)\b', 'metricAh', text)
        text = re.sub(r'\b[\d\.\/]+\s?(in|inch|inches)\b', 'metricIn', text)
        text = re.sub(r'\b[\d\.\/]+\s?\"', 'metricIn', text)
        text = re.sub(r'\b[\d\.\/]+\s?(gb|gig|go|giga|gigabit|gigabyte)\b', 'metricGb', text)
        text = re.sub(r'\b[\d\.\/]+\s?(oz|ounce)\b', 'metricOz', text)
        text = re.sub(r'\b[\d\.\/]+\s?(fl\.? oz\.?|fluids? ounces?)\b', 'metricFlOz', text)
        text = re.sub(r'\b[\d\.\/]+\s?(cwt|quintal)\b', 'metricCwt', text)
        text = re.sub(r'\b[\d\.\/]+\s?(mhz|hz|khz|ghz|gigahertz|megahertz|kilohertz|hertz)\b', 'metricHz', text)
        text = re.sub(r'\b[\d\.\/]+\s?(wh|kwh|watt-hour|kilowatt-hour)\b', 'metricWh', text)
        text = re.sub(r'\b[\d\.\/]+\s?(w|kw|watt|kilowatt)\b', 'metricW', text)
        text = re.sub(r'\b[\d\.\/]+\s?(mf|mfd|mmf|mmfd|microfarad)\b', 'metricMfd', text)
        text = re.sub(r'\b[\d\.\/]+\s?(ft|feet|foot)\b', 'metricFt', text)
        text = re.sub(r'\b[\d\.\/]+\s?(cm|centimeter)\b', 'metricCm', text)
        text = re.sub(r'\b[\d\.\/]+\s?(mm|millimeter)\b', 'metricMm', text)
        text = re.sub(r'\b[\d\.\/]+\s?(km|kilometer)\b', 'metricKm', text)
        text = re.sub(r'\b[\d\.\/]+\s?(m|meter)\b', 'metricM', text)
        text = re.sub(r'\b[\d\.\/]+\s?(cell|cells)\b', 'metricCell', text)
        text = re.sub(r'\b[\d\.\/]+\s?(lb|lbs|pound)\b', 'metricLb', text)
        text = re.sub(r'\b[\d\.\/]+\s?(yds|yd|yard|yards)\b', 'metricYd', text)
        text = re.sub(r'\b[\d\.\/]+\s?(pc|pcs|pieces|piece)\b', 'metricPc', text)
        text = re.sub(r'\b[\d\.\/]+\s?(gal|gals|gallon|gallons)\b', 'metricGal', text)
        text = re.sub(r'\b[\d\.\/]+\s?(yd|yds|yard|yards)\b', 'metricYd', text)
        text = re.sub(r'\b[\d\.\/]+\s?(deg|degs|degree|degrees)\b', 'metricDeg', text)
        text = re.sub(r'\b[\d\.\/]+\s?\°', 'metricDeg', text)
        text = re.sub(r'\b[\d\.\/]+\s?(l|liter|liters)\b', 'metricL', text)
        text = re.sub(r'\b[\d\.\/]+\s?(ml|mls|milliliter|milliliters)\b', 'metricMl', text)
        text = re.sub(r'\b[\d\.\/]+\s?(kg|kilograms|kilogram)\b', 'metricKg', text)
        text = re.sub(r'\b[\d\.\/]+\s?(g|grams|gram)\b', 'metricG', text)
        text = re.sub(r'\b[\d\.\/]+\s?(mg|mgs|milligrams|milligram)\b', 'metricMg', text)
        text = re.sub(r'\b[\d\.\/]+\s?(sq|sqs|square|squares)\b', 'metricSq', text)
        text = re.sub(r'\b[\d\.\/]+\s?(pt|pts|pint|pints)\b', 'metricPt', text)
        text = re.sub(r'\b[\d\.\/]+\s?(ohm)\b', 'metricOhm', text)
        text = re.sub(r'\b[\d\.\/]+\s?(fz)\b', 'metricFz', text)
        text = re.sub(r'\b[\d\.\/]+\s?(ct|cts|carat|carats)\b', 'metricCt', text)
        text = re.sub(r'\b[\d]+p\b', 'metricRes', text)
        text = re.sub(r'\b[\d]+x[\d]+\b', 'metricRes', text)
        text = re.sub(r'\b[\d]+x\b', 'metricX', text)
        
        self.text = text
        return self.text

    def lemmatize(self, text=None):
        """Function cuts  end of a words such that only the lemma(root) remains

        Uses NLTK's WordNetLemmatizer() in present form
        
        Note:
            function also update the class variable ``text``

        Examples:
            >>> print(lemmatize('I am writing too long docstrings'))
            I be write too long docstrings

        Args:
            text (str) : text to preprocess
        
        Returns:
            str:  text with all the words brough to their root form(lemma)
        """
        if text is None:
            text = self.text

        self.text= ' '.join([WordNetLemmatizer().lemmatize(word, pos="v") for word in text.split()])
        return self.text

        
    def pipeline(self, text=None, methods=None):
        """Function sequential executes all the functions given in ``methods`` list

        the options for preprocessing functions are: |br|
        1. make_lowercase |br| 
        2. remove_stopwords |br|
        3. remove_extra_spaces |br|
        4. remove_punctuations_and_symbols |br|
        5. remove_digits |br|
        6. standardize_metrics |br|
        7. lemmatize |br|


        Note:
            function also update the class variable ``text``

        Examples:
            >>> print(pipeline('Prepocess Me 123 !@3 23V', methods=['make_lowercase', 'remove_digits', 'remove_punctuations_and_symbols']))
            prepocess me 3 23v

        Args:
            text (str) : text to preprocess
            methods (:obj:`list` of :obj:`str`): list of functions to execute 
        
        Returns:
            str:  text after applyind all the methods

        Raises:
            NameError: if any of functions in ``methods`` isn't from allowed options
        """
        AWAILABLE_METHODS = ['make_lowercase', 'remove_stopwords', \
                             'remove_extra_spaces', 'remove_punctuations_and_symbols', \
                             'remove_digits', 'standardize_metrics', 'lemmatize']

        if text is None:
            text = self.text
        if methods is None:
            methods = self.methods
        
        for method in methods:
            if method not in AWAILABLE_METHODS:
                raise NameError(f'you used {method} function which in not in {AWAILABLE_METHODS} list')
            else:
                text = getattr(Preprocessor, method)(self, text)
        
        self.text = text
        return text
