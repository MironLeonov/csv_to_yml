import pandas as pd
import datetime


class Converter:

    def __init__(self, csv_file_path, yml_file_path):
        self.data_yml = open(yml_file_path, 'w', encoding="utf-8")
        self.data_csv = pd.read_csv(csv_file_path, delimiter=';', encoding='cp1251')

    def header(self):
        now_time = datetime.datetime.now()
        self.data_yml.write('<yml_catalog' + ' date=' + '"' + now_time.strftime("%d-%m-%Y %H:%M") + '"' + '>' + "\n")
        self.data_yml.write('<shop>\n')

    def basic_information(self):
        for column in self.data_csv:
            if column == 'category':
                break
            self.data_yml.write("<" + column + ">" + self.data_csv[column][0] + "</" + column + ">\n")

    def tag_params(self, tag, delimiter):
        params = []
        for column in self.data_csv:
            if f'{tag}{delimiter}' in column:
                params.append(column)
        return params

    def write_tag(self, tag, params, i):
        if 'param' in tag:
            self.data_yml.write('<param')
            self.data_yml.write(' ' + 'name=' + '"' + tag[5:] + '"')
        else:
            self.data_yml.write(f'<{tag}')

        for param in params:
            if str(self.data_csv[param][i]) != "nan":
                self.data_yml.write(' ' + param.split('_')[1] + '=' + '"' + str(self.data_csv[param][i]).lower() + '"')

    def write_sub_tag(self, sub_tags, i):
        for tag in sub_tags:
            if str(self.data_csv[tag][i]) != "nan":
                params = self.tag_params(tag.split('-')[1], '_')
                self.write_tag(tag.split('-')[1], params, i)
                if 'param' in tag:
                    self.data_yml.write(">" + str(self.data_csv[tag][i]) + '</' + tag.split('-')[1][:5] + '>\n')
                else:
                    self.data_yml.write(">" + str(self.data_csv[tag][i]) + '</' + tag.split('-')[1] + '>\n')

    def categories(self):
        self.data_yml.write('<categories>\n')

        category_params = self.tag_params('category', '_')

        for i in range(self.data_csv['category'].dropna().size):
            self.write_tag('category', category_params, i)
            self.data_yml.write(">" + self.data_csv['category'][i] + '</category>\n')

        self.data_yml.write('</categories>\n')

    def offers(self):
        self.data_yml.write('<offers>\n')
        offers_params = self.tag_params('offer', '-')
        offer_params = self.tag_params('offer', '_')
        for i in range(self.data_csv['offer_id'].dropna().size):
            self.write_tag('offer', offer_params, i)
            self.data_yml.write('>\n')
            self.write_sub_tag(offers_params, i)
            self.data_yml.write("</offer>\n")

        self.data_yml.write('</offers>\n')

    def footer(self):
        self.data_yml.write('</shop>\n')
        self.data_yml.write('</yml_catalog>')
        self.data_yml.close()

    def convert(self):
        self.header()
        self.categories()
        self.offers()
        self.footer()


if __name__ == '__main__':
    converter = Converter('data.csv', 'data.xml')
    converter.convert()
