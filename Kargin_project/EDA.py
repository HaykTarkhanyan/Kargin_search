import numpy as np
import pandas as pd
import plotly.express as px


class EDA:
    """
    Description
    -----------
    Takes in DataFrame and returns dictionary with interesting labels as keys and their values as dict values
    Parameters
    ----------
    df: DataFrame
        DataFrame with kargin rows
        
    Methods
    -------
    bla bla bla
    """

    def __init__(self, df, new_df):
        self.df = df
        self.new_df = new_df
        
    def most_relevant_place(self):
        """
        Return most relevant place and quantity
        """
        return self.df['Վայր'].value_counts().index[0], self.df['Վայր'].value_counts()[0]
    
    def most_relevant_couple(self):
        """
        Return most relevant couple/triple and quantity
        """
        return self.df['Հիմնական դերասաններ'].value_counts().index[1], self.df['Հիմնական դերասաններ'].value_counts()[1]
    
    def histogram_column(self, column="Վայր"):
        """
        Takes in column name with which one we want to visualize histogram
        Parameters
        ----------
        column: {"Լեզուներ", "Վայր", "հիմնական դերասանների քանակ"}, default="Վայր"
        """
        if not column in {"Լեզուներ", "Վայր", "հիմնական դերասանների քանակ"}:
            raise ValueError("""Invalid value.  Please choose one of the set: {"Լեզուներ", "Վայր", "հիմնական դերասանների քանակ"}""")
       
        fig = px.histogram(self.df[column].dropna().sort_index(), x=column, title=column.capitalize()).update_xaxes(categoryorder="total descending")
        fig.show()
        
    def longest_text(self):
        """
        Returns longest text and his length
        """
        df = self.df[~self.df['Տեքստ'].isna()]
        df.index = range(len(df))
        lst = []
        for i in df['Տեքստ'].index:
            lst.append(len(df['Տեքստ'][i]))

        return df["links"][lst.index(max(lst))], max(lst)
    
    def most_min_n_viewed_or_sth(self, typee="most", column_name="views", n=3, reset_index=True):
        """
        Returns DataFrame of n most/least viewed/liked/disliked/commented kargin videos
        
        Parameters
        ----------
        typee: {"most", "least"}, default="most"
        
        column_name: {"views", "likes", "dislikes", "comments"}
        
        n: int, quantity of videos, default=3
        
        reset_index: bool, default=True
            Whether or not reset new DataFrame indices
        """
        # Validation of values
        if not typee in {"most", "least"}:
            raise ValueError("""Invalid value.  Please choose one of the set: ["most", "least"]""")
        if not column_name in {"views", "likes", "dislikes", "comments"}:
            raise ValueError("""Invalid value.  Please choose one of the set: {"views", "likes", "dislikes", "comments"}""")
        if type(n) != int or n < 1:
            raise ValueError(f"Expected n as an integer >0, got {n}")
        if type(reset_index) != bool:
            raise ValueError(f"Value of reset_index expected boolean, got {reset_index}")
        

        # printing DataFrame   
        if typee == "most":
            if reset_index == True:
                if not column_name in {"likes", "dislikes"}:   # print inputs
                    print(f"{n} {typee} {column_name[:-1]}ed kargin videos.")
                else:
                    print(f"{n} {typee} {column_name[:-1]}d kargin videos.")                    
                return self.new_df.loc[self.new_df[column_name][np.argsort(self.new_df[column_name])][-n:][::-1].index].reset_index()
            else:
                if not column_name in {"likes", "dislikes"}:   # print inputs
                    print(f"{n} {typee} {column_name[:-1]}ed kargin videos.")
                else:
                    print(f"{n} {typee} {column_name[:-1]}d kargin videos.")
                return self.new_df.loc[self.new_df[column_name][np.argsort(self.new_df[column_name])][-n:][::-1].index]
        else:
            if reset_index == True:
                if not column_name in {"likes", "dislikes"}:   # print inputs
                    print(f"{n} {typee} {column_name[:-1]}ed kargin videos.")
                else:
                    print(f"{n} {typee} {column_name[:-1]}d kargin videos.")
                return self.new_df.loc[self.new_df[column_name][np.argsort(self.new_df[column_name])][:n].index].reset_index()
            else:
                if not column_name in {"likes", "dislikes"}:   # print inputs
                    print(f"{n} {typee} {column_name[:-1]}ed kargin videos.")
                else:
                    print(f"{n} {typee} {column_name[:-1]}d kargin videos.")
                return self.new_df.loc[self.new_df[column_name][np.argsort(self.new_df[column_name])][:n].index]      
    
    def get_stats(self):
        """
        Returns dictionary with interesting labels as keys and their values as dict values
        """
        stats = {}
        stats["Ամենահաճախ հանդիպող վայրը"] = self.most_relevant_place()[0]
        stats["Ամենահաճախ հանդիպող զույգ"] = self.most_relevant_couple()[0]
        stats["Ամենաերկար կարգինը աշխարհում"] = self.longest_text()[0]

        return 
