import os


def append_figures(figures_list, figure_type, figure_text):
    page_text = ""
    for figure in figures_list:
        if figure.find(figure_type) == -1:
            continue
        figure_name = figure.strip("plot_"+figure_type).rstrip(".png")
        page_text += '<a name="'+figure_name+'">'+figure_name+' '+figure_text+'</a>\n'
        page_text += "---------------\n"
        page_text += '![alt text](\static\\'+figure+' "'+figure_name+' '+figure_text+'")\n\n'
    return page_text


def build_page():
    content = """
    Twitter Scraper
    ===============

    """
    figures_list = [x for x in os.listdir("./static/") if x.find(".png") != -1]
    for figure in figures_list:
        if figure.find("24_hours") != -1:
            figure_name = figure.strip("plot_24_hours").rstrip(".png")
            content += "* ["+figure_name+" last 24 hours](#"+figure_name+")\n"
        else:
            figure_name = figure.strip("full").rstrip(".png")
            content += "* [" + figure_name + " full](#" + figure_name + ")\n"
    content += "\n"
    content += append_figures(figures_list, "24_hours", "last 24 hours")
    content += append_figures(figures_list, "full", "full")
    return content
