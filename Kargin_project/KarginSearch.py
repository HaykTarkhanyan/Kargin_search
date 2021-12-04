import pandas as pd
from fuzzywuzzy import fuzz


class KarginSearch:
    def __init__(self, query, filters, data):
        self.query = query
        self.filters = filters
        self.data = data

    def apply_filters(self):
        mask = pd.Series([True] * len(self.data))

        if "Հիմնական դերասաններ" in self.filters:
            mask &= self.data["Հիմնական դերասաններ"].apply(lambda x: set(self.filters["Հիմնական դերասաններ"]) <= x)
        if "հիմնական դերասանների քանակ" in self.filters:
            mask &= self.data["հիմնական դերասանների քանակ"] == self.filters["հիմնական դերասանների քանակ"]
        if "Դերերի անուններ" in self.filters:
            mask &= self.data["Դերերի անուններ"].apply(lambda x: set(self.filters["Դերերի անուններ"]) <= x)
        if "Վայր" in self.filters:
            mask &= self.data["Վայր"] == self.filters["Վայր"]
        if "Լուսավորվածություն" in self.filters:
            mask &= self.data["Լուսավորվածություն"] == self.filters["Լուսավորվածություն"]
        if "Լեզուներ" in self.filters:
            mask &= self.data["Լեզուներ"] == self.filters["Լեզուներ"]

        return self.data[mask]

    def exact_search(self):
        # debug purposes; remove later
        # self.data = pd.read_csv("../Կարգին 2+3րդ փլեյլիստ - Sheet3.csv").dropna(subset=["Տեքստ"])

        # TODO:
        # preprocess self.data or have it preprocessed in advance

        # TODO:
        # change "Տեքստ" to something less meaningless

        mask = self.data["Տեքստ"].str.contains(self.query)

        # change this behavior if needed
        # (hint: don't)
        return self.data[mask] if mask.any() else None

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

    def fuzzy_search(self):
        # TODO:
        # replace "Տեքստ" with sth more meaningful
        self.data["similarity_score"] = self.data["Տեքստ"].apply(KarginSearch.get_similarity_score,
                                                                 keyword_input=self.query)
        self.data = self.data.sort_values("similarity_score", ascending=False)
        return self.data

    def find(self):
        self.data = self.apply_filters()
        results = self.exact_search() or self.fuzzy_search()
        return results
