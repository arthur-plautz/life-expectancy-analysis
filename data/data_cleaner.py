import pandas as pd

class DataCleaner:
    def __init__(self):
        self.raw_dir = 'raw'
        self.clean_dir = 'clean'

    def reset_index(self, df):
        return df.reset_index(drop=True, col_fill=[i for i in range(len(df))])

    def get_df(self, df):
        return pd.read_csv(f'{self.raw_dir}/{df}.csv')
    
    def who_source_rename(self, df, col_line=1):
        new_cols = df.loc[col_line]
        old_cols = df.columns
        df = df.rename(columns=self.cols_map(new_cols, old_cols))
        df = df.drop([i for i in range(col_line+1)])
        df = self.reset_index(df)
        return df

    def cols_map(self, new_cols, old_cols):
        map_cols = {}
        for i in range(len(old_cols)):
            map_cols[old_cols[i]] = new_cols[i].lower().replace(' ', '_')
        return map_cols

    def air_polution(self):
        def transform(total):
            col = []
            for line in total:
                t = float(line.split('[')[0])
                col.append(t)
            return col
        df = self.get_df('air_polution')
        df = self.who_source_rename(df)
        df = df.drop([0,1])
        df = self.reset_index(df)
        df['total'] = transform(df['total'])
        return df[['country', 'total']]

    def basic_sanitation(self):
        def transform(percentage):
            return [float(l) for l in percentage]
        df = self.get_df('basic_sanitation')
        df = df[[df.columns[0], '2016']]
        df = self.who_source_rename(df)
        df = df.drop([0,1])
        df = self.reset_index(df)
        df['total'] = transform(df['total'])
        return df

    def inequality(self):
        def transform(percentage):
            return [float(l) for l in percentage]
        df = self.get_df('inequality')
        df = df.rename(columns={'giniCoefficient': 'coef'})
        df['coef'] = transform(df['coef'])
        return df[['country', 'coef']]

    def life_expectancy(self):
        def transform(age):
            return [float(l) for l in age]
        df = self.get_df('life_expectancy')
        df = df[[df.columns[0], df.columns[1], df.columns[5]]]
        df = self.who_source_rename(df, col_line=0)
        df = df.query('year == "2019"')
        df = self.reset_index(df)
        df = df.rename(columns={'both_sexes': 'total'})
        df['total'] = transform(df['total'])
        return df[['country', 'total']]

    def mortality(self):
        def transform(mortality):
            return [int(l) for l in mortality]
        df = self.get_df('mortality')
        df = self.who_source_rename(df, col_line=0)
        df = df.query('year == "2016"')
        df = self.reset_index(df)
        df = df.rename(columns={'both_sexes': 'total'})
        return df[['country', 'total']]

    def violence(self):
        def transform(total):
            col = []
            for line in total:
                t = int(line.split('[')[0])
                col.append(t)
            return col
        df = self.get_df('violence')
        df = df[[df.columns[0], df.columns[1]]]
        df = self.who_source_rename(df)
        df = self.reset_index(df)
        df = df.rename(columns={'both_sexes': 'total'})
        df['total'] = transform(df['total'])
        return df[['country', 'total']]

    def water_quality(self):
        def transform(percentage):
            return [float(l) for l in percentage]
        df = self.get_df('water_quality')
        df = df[[df.columns[0], df.columns[1]]]
        df = self.who_source_rename(df)
        df['total'] = transform(df['total'])
        return df[['country', 'total']]

    def rmnch_by_wealth(self):
        def get_better_data(df):
            srcs = []
            for src in df['data_source'].unique():
                df_src = df.query(f'data_source == "{src}"')
                src_by_year = []
                for y in df_src.year:
                    value = 0
                    i = 0
                    df_src_y = df_src.query(f'year == {y}')
                    for c in range(3, 13):
                        v = df_src_y[df.columns[c]]
                        if v.unique()[0] != 'No data':
                            value += 1
                        i += 1
                    src_by_year.append({'s': src, 'q': float(value/i), 'y': y})
                df_src_by_year = pd.DataFrame(src_by_year)
                df_src_by_year = df_src_by_year.sort_values('q', ascending=False)
                df_src_by_year = self.reset_index(df_src_by_year)
                s = df_src_by_year.loc[0]['s']
                q = df_src_by_year.loc[0]['q']
                y = df_src_by_year.loc[0]['y']
                srcs.append({'s': s, 'q': q, 'y': y})
            df_srcs = pd.DataFrame(srcs)
            df_srcs = df_srcs.sort_values('q', ascending=False)
            src = df_srcs.loc[0]['s']
            year = df_srcs.loc[0]['y']
            return df.query(f'data_source == "{src}" & year == {year}')

        def get_latest_data(df):
            latest_data = []
            countries = df['country'].unique()
            for c in countries:
                country = df.query(f'country == "{c}"')
                country['year'] = [int(y) for y in country['year']]
                country = get_better_data(country)
                df_c = country.sort_values('year', ascending=False)
                df_c = self.reset_index(df_c)
                latest_data.append(df_c.loc[0])
            return pd.DataFrame(latest_data)
        
        def deciles_mean(df):
            data = []
            for row in df.to_records():
                deciles_sum = 0
                deciles_count = 0
                for c in range(4,14):
                    value = row[c]
                    if value != "No data":
                        deciles_sum += float(value)
                        deciles_count += 1
                if deciles_count > 0:
                    data.append(deciles_sum/deciles_count)
                else:
                    data.append("No data")
            df['mean'] = data
            return df

        df = self.get_df('rmnch_wealth')
        df = self.who_source_rename(df, col_line=0)
        df = get_latest_data(df)
        df = deciles_mean(df)
        df = df.query('mean != "No data"')
        df = self.reset_index(df)
        return df[['country', 'mean']]

    def format(self):
        def transpose_col(df, country, target):
            df_country = df.query(f'country == "{country}"')
            return float(df_country[target]) if not df_country[target].empty else None
        dfs = {
            'life_expectancy': {
                'df': self.life_expectancy(),
                'target': 'total'
            },
            'rmnch_by_wealth': {
                'df': self.rmnch_by_wealth(),
                'target': 'mean'
            },
            'air_polution': {
                'df': self.air_polution(),
                'target': 'total'
            },
            'basic_sanitation': {
                'df': self.basic_sanitation(),
                'target': 'total'
            },
            'inequality': {
                'df': self.inequality(),
                'target': 'coef'
            },
            'mortality': {
                'df': self.mortality(),
                'target': 'total'
            },
            'violence': {
                'df': self.violence(),
                'target': 'total'
            },
            'water_quality': {
                'df': self.water_quality(),
                'target': 'total'
            }
        }
        data = []
        for country in dfs['rmnch_by_wealth']['df'].country:
            row = {'country': country}
            for col, info in dfs.items():
                df = info['df']
                row[col] = transpose_col(df, country, info['target'])
            data.append(row)
        return pd.DataFrame(data).dropna()

    def clean(self):
        df = self.format()
        df = self.reset_index(df)
        print(df)
        # df.to_csv(f"{self.clean_dir}/life_expectancy_analysis.csv")

dc = DataCleaner()
dc.clean()