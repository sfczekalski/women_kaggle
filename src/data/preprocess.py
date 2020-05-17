import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np
import warnings


def preprocess_data(data_folder):
    warnings.filterwarnings('ignore')
    df = pd.read_csv(data_folder + 'raw/multiple_choice_responses.csv', header=1)
    _ = df.pop('Duration (in seconds)')

    df.rename(columns={'What is your gender? - Selected Choice': 'Gender'}, inplace=True)
    df.rename(columns={'Select the title most similar to your current role (or most recent title if retired): - Selected Choice': 'Job title'}, inplace=True)
    country_col = 'In which country do you currently reside?'
    df.loc[df[country_col]=='United States of America', country_col] = 'USA'
    df.loc[df[country_col]=='United Kingdom of Great Britain and Northern Ireland', country_col] = 'UK'
    df.loc[df[country_col]=='Iran, Islamic Republic of...', country_col] = 'Iran'

    df.to_csv(data_folder + 'processed/data.csv', index=False)


def preprocess_skills_data(data_folder):
    # Create subsets of variable dedicated to skills, activities, programming languages etc.
    ide_usage = ["Q16_Part_1", "Q16_Part_2", "Q16_Part_3", "Q16_Part_4", "Q16_Part_5", "Q16_Part_6", "Q16_Part_7",
                 "Q16_Part_8", "Q16_Part_9", "Q16_Part_10"]
    notebook_usage = ["Q17_Part_1", "Q17_Part_2", "Q17_Part_3", "Q17_Part_4", "Q17_Part_5", "Q17_Part_6", "Q17_Part_7",
                      "Q17_Part_8", "Q17_Part_9", "Q17_Part_10"]
    language_usage = ["Q18_Part_1", "Q18_Part_2", "Q18_Part_3", "Q18_Part_4", "Q18_Part_5", "Q18_Part_6", "Q18_Part_7",
                      "Q18_Part_8", "Q18_Part_9", "Q18_Part_10"]
    visual_usage = ["Q20_Part_1", "Q20_Part_2", "Q20_Part_3", "Q20_Part_4", "Q20_Part_5", "Q20_Part_6", "Q20_Part_7",
                    "Q20_Part_8", "Q20_Part_9", "Q20_Part_10"]
    algo_usage = ["Q24_Part_1", "Q24_Part_2", "Q24_Part_3", "Q24_Part_4", "Q24_Part_5", "Q24_Part_6", "Q24_Part_7",
                  "Q24_Part_8", "Q24_Part_9", "Q24_Part_10"]
    ml_tools_usage = ["Q25_Part_1", "Q25_Part_2", "Q25_Part_3", "Q25_Part_4", "Q25_Part_5", "Q25_Part_6"]
    cv_usage = ["Q26_Part_1", "Q26_Part_2", "Q26_Part_3", "Q26_Part_4", "Q26_Part_5"]
    nlp_usage = ["Q27_Part_1", "Q27_Part_2", "Q27_Part_3", "Q27_Part_4"]
    ml_frameworks_usage = ["Q28_Part_1", "Q28_Part_2", "Q28_Part_3", "Q28_Part_4", "Q28_Part_5", "Q28_Part_6",
                           "Q28_Part_7", "Q28_Part_8", "Q28_Part_9", "Q28_Part_10"]
    cloud_platforms_usage = ["Q29_Part_1", "Q29_Part_2", "Q29_Part_3", "Q29_Part_4", "Q29_Part_5", "Q29_Part_6",
                             "Q29_Part_7", "Q29_Part_8", "Q29_Part_9", "Q29_Part_10"]
    cloud_products_usage = ["Q30_Part_1", "Q30_Part_2", "Q30_Part_3", "Q30_Part_4", "Q30_Part_5", "Q30_Part_6",
                            "Q30_Part_7", "Q30_Part_8", "Q30_Part_9", "Q30_Part_10"]
    big_data_products_usage = ["Q31_Part_1", "Q31_Part_2", "Q31_Part_3", "Q31_Part_4", "Q31_Part_5", "Q31_Part_6",
                               "Q31_Part_7", "Q31_Part_8", "Q31_Part_9", "Q31_Part_10"]
    ml_products_usage = ["Q32_Part_1", "Q32_Part_2", "Q32_Part_3", "Q32_Part_4", "Q32_Part_5", "Q32_Part_6",
                         "Q32_Part_7", "Q32_Part_8", "Q32_Part_9", "Q32_Part_10"]
    automl_tools = ["Q33_Part_1", "Q33_Part_2", "Q33_Part_3", "Q33_Part_4", "Q33_Part_5", "Q33_Part_6", "Q33_Part_7",
                    "Q33_Part_8", "Q33_Part_9", "Q33_Part_10"]
    db_tools = ["Q34_Part_1", "Q34_Part_2", "Q34_Part_3", "Q34_Part_4", "Q34_Part_5", "Q34_Part_6", "Q34_Part_7",
                "Q34_Part_8", "Q34_Part_9", "Q34_Part_10"]

    gender_question = ["Q2"]

    # Dataframe with skills related questions
    df_skills = pd.read_csv('../data/raw/multiple_choice_responses.csv')
    skills = [gender_question, ide_usage, notebook_usage, language_usage, visual_usage, cloud_products_usage, algo_usage,
              ml_tools_usage, cv_usage, nlp_usage, ml_frameworks_usage, cloud_platforms_usage,
              big_data_products_usage, ml_products_usage, automl_tools, db_tools]
    df_skills = df_skills.loc[:, np.concatenate(skills)]

    # Questions as column names
    df_skills.columns = df_skills.iloc[0]
    df_skills.drop(df_skills.index[0], inplace=True)
    df_skills = df_skills.reset_index(drop=True)

    # Analize only female kagglers
    df_skills = df_skills[df_skills['What is your gender? - Selected Choice'] == 'Female']
    df_skills.drop(columns=['What is your gender? - Selected Choice'], inplace=True)

    # Shorten column names - only a skill name
    for c in df_skills.columns:
        column_name = c.split('Selected Choice - ')[-1].strip().split('(')[0]
        df_skills.rename(columns={c: column_name}, inplace=True)

    # Binarize
    df_skills[~df_skills.isnull()] = 1
    df_skills[df_skills.isnull()] = 0
    df_skills = df_skills.astype(np.int8)

    df_skills.to_csv(data_folder + 'processed/skills_data.csv', index=False)
