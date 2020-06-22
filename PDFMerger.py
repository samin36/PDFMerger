import PySimpleGUI as sg
import PyPDF4


def merge_pdfs(files, output_file):
    try:
        pdf_merger = PyPDF4.PdfFileMerger()
        for file in files:
            pdf_reader = PyPDF4.PdfFileReader(open(file, 'rb'), strict=False)
            pdf_merger.append(pdf_reader)
        if not output_file.endswith('.pdf'):
            output_file = f'{output_file}.pdf'
        pdf_merger.write(output_file)
        pdf_merger.close()
        return 1
    except Exception as e:
        return 0


if __name__ == '__main__':
    sg.theme('DarkTeal2')
    layout = [[sg.Text('***The files are merged in alphabetical order')],
              [sg.Listbox(values=[], key='Files', size=(100, 20), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
              [sg.FileSaveAs(file_types=(('PDF', '*.pdf'),)), sg.Input(key='OutputFile'), ],
              [sg.Input(key='TempInput', visible=False, enable_events=True),
               sg.FilesBrowse(file_types=(('PDF', '*.pdf'),)), sg.Button('Merge'), sg.Button('Cancel')]]

    window = sg.Window('PDF Merger', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == 'TempInput':
            if values.get('TempInput'):
                files = values.get('TempInput').split(';')
                window['Files'].Update(values=files)
        elif event == 'Merge':
            if not window['Files'].get_list_values():
                sg.popup('No files selected')
            elif not values.get('OutputFile', ''):
                sg.popup('Please select the output file location and name')
            else:
                return_code = merge_pdfs(window['Files'].get_list_values(), values.get('OutputFile'))
                popup_message = f'Merged {"Successfully" if return_code == 1 else "Failed"}'
                sg.popup(popup_message)
                break
    window.close()
