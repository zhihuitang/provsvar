import pandas as pd
import openpyxl as pxl
from openpyxl.styles import Alignment
import os
import shutil

origin_provsvar_file_name = 'Provsvar.xlsx'
output_file_name = 'Provsvar-summary.xlsx'
references_df = pd.read_excel("References.xlsx")


class LabReference:
    def __init__(self, name, min, max):
        self.name = name
        self.min = min
        self.max = max


# Provsvar-fixed
provsvar_df = pd.read_excel(origin_provsvar_file_name, sheet_name='Sheet1', index_col=0)

bad_style_low = 'background-color: #FFFB00'
bad_style_high = 'background-color: #FFC7CE'


def get_style(*, val, reference):
    if not isinstance(val, int) and not isinstance(val, float):
        return ''
    if val < reference.min:
        return bad_style_low
    elif val > reference.max:
        return bad_style_high
    else:
        return ''


lab_references = []
for i, row in references_df.iterrows():
    '''
    Name	                            Min	Max
    Datum		
    S-ACE (E/L)                     	0	70
    P--25-OH Vitamin D2+D3 (nmol/L)	    50	250
    S-1,25-OH-Vitamin D (pmol/L)	    48	190
    ......
    
    '''
    lab_item = LabReference(row['Name'], row['Min'], row['Max'])
    lab_references.append(lab_item)


for row in provsvar_df.index:
    for lab_item in lab_references:
        value = provsvar_df[lab_item.name].at[row]
        if isinstance(value, str):
            # Fix abnormal cell: "0,33, 0,33", convert "," to "."            
            try: 
                provsvar_df[lab_item.name].at[row] = float(value.split(", ")[0].replace(",", "."))
            except ValueError:
                provsvar_df[lab_item.name].at[row] =  value

headers = list(map(lambda x: x.name, lab_references))

provsvar_new_df = pd.DataFrame(provsvar_df, columns=headers)

provsvar_new_df.style.set_properties(**{'background-color': 'white',
                                     'color': 'black',
                                     'border-color': 'black',
                                     'border-width': '1px',
                                     'border-style': 'solid'}) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[1]), subset=[lab_references[1].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[1]), subset=[lab_references[1].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[2]), subset=[lab_references[2].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[3]), subset=[lab_references[3].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[4]), subset=[lab_references[4].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[5]), subset=[lab_references[5].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[6]), subset=[lab_references[6].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[7]), subset=[lab_references[7].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[8]), subset=[lab_references[8].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[9]), subset=[lab_references[9].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[10]), subset=[lab_references[10].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[11]), subset=[lab_references[11].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[12]), subset=[lab_references[12].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[13]), subset=[lab_references[13].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[14]), subset=[lab_references[14].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[15]), subset=[lab_references[15].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[16]), subset=[lab_references[16].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[17]), subset=[lab_references[17].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[18]), subset=[lab_references[18].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[19]), subset=[lab_references[19].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[20]), subset=[lab_references[20].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[21]), subset=[lab_references[21].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[22]), subset=[lab_references[22].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[23]), subset=[lab_references[23].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[24]), subset=[lab_references[24].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[25]), subset=[lab_references[25].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[26]), subset=[lab_references[26].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[27]), subset=[lab_references[27].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[28]), subset=[lab_references[28].name]) \
    .applymap(lambda x: get_style(val=x, reference=lab_references[29]), subset=[lab_references[29].name]) \
    .to_excel(output_file_name, engine='openpyxl', sheet_name='Summary', index=True)

provsvar_new_workbook = pxl.load_workbook(output_file_name)
worksheet = provsvar_new_workbook['Summary']
worksheet.freeze_panes = 'B2'

# set first column width
worksheet.column_dimensions['A'].width = 18

# set wrapText for the fist row
for cell in worksheet[1]:
    cell.alignment = Alignment(wrapText=True)

# write References
with pd.ExcelWriter(output_file_name, engine='openpyxl') as writer:
    writer.book = provsvar_new_workbook
    writer.sheets = {
        worksheet.title: worksheet for worksheet in provsvar_new_workbook.worksheets
    }
    references_df.to_excel(writer, 'References', index=False)
    references_worksheet = provsvar_new_workbook['References']
    references_worksheet.freeze_panes = 'B2'
    references_worksheet.column_dimensions['A'].width = 30
    writer.save()

current_path = os.getcwd()
shutil.copy(f'{current_path}/{output_file_name}', f'/Users/zhihuitang/Dropbox/Medical/{output_file_name}')

print("complete")

