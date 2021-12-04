import pandas as pd
from fuzzywuzzy import fuzz


class KarginSearch:
    def __init__(self, data):
        self.data = data

    def apply_filters(self, filters):
        mask = pd.Series([True] * len(self.data))

        if "Հիմնական դերասաններ" in filters:
            mask &= self.data["Հիմնական դերասաններ"].apply(lambda x: set(filters["Հիմնական դերասաններ"]) <= x)
        if "հիմնական դերասանների քանակ" in filters:
            mask &= self.data["հիմնական դերասանների քանակ"] == filters["հիմնական դերասանների քանակ"]
        if "Դերերի անուններ" in filters:
            mask &= self.data["Դերերի անուններ"].apply(lambda x: set(filters["Դերերի անուններ"]) <= x)
        if "Վայր" in filters:
            mask &= self.data["Վայր"] == filters["Վայր"]
        if "Լուսավորվածություն" in filters:
            mask &= self.data["Լուսավորվածություն"] == filters["Լուսավորվածություն"]
        if "Լեզուներ" in filters:
            mask &= self.data["Լեզուներ"] == filters["Լեզուներ"]

        return self.data[mask]

    def exact_search(self, query, data):
        # debug purposes; remove later
        # self.data = pd.read_csv("../Կարգին 2+3րդ փլեյլիստ - Sheet3.csv").dropna(subset=["Տեքստ"])

        # TODO:
        # preprocess self.data or have it preprocessed in advance

        # TODO:
        # change "Տեքստ" to something less meaningless

        mask = data["Տեքստ"].str.contains(query)

        # change this behavior if needed
        # (hint: don't)
        return data[mask] if mask.any() else None

    @staticmethod
    def get_similarity_score(keyword_base, keyword_input):
        """Function computes how similar 2 words are.
        Notes:
            Equation is 0.3 * ratio + 0.3 * partial_ratio + 0.4 * token_set_ratio
        Args:
            keyword_base (str)
            keyword_input (str)
        Returns:
            float: value between 0 and 100.

        Examples:
            >>> print (get_similarity_score('varsik', 'tandzik'))
            47.2
        """
        a = fuzz.ratio(keyword_input, keyword_base)
        b = fuzz.partial_ratio(keyword_input, keyword_base)
        c = fuzz.token_set_ratio(keyword_input, keyword_base)

        score = 0.3 * a + 0.3 * b + 0.4 * c
        return score

    def fuzzy_search(self, query, data):
        # TODO:
        # replace "Տեքստ" with sth more meaningful
        data["similarity_score"] = data["Տեքստ"].apply(KarginSearch.get_similarity_score, keyword_input=query)
        data = data.sort_values("similarity_score", ascending=False)
        return data

    def find(self, query, filters):
        data = self.apply_filters(filters)

        # TODO:
        # replace the following lines with
        # `results = self.exact_search(data, query) or self.fuzzy_search(data, query)`
        # whenever the world becomes full of գեղեցկությունը հարգող տղա's
        results = self.exact_search(data, query)
        if results is None:
            results = self.fuzzy_search(data, query)

        return results
