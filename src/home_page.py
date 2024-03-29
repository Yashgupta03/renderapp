import dash
from dash import html


# Main page layout
h_home_page=html.Div(
    children=[
        html.Div(
            className="header",
            children=[
                html.H1("Indo Aryan Language Distribution"),
                html.P("Brief Overview on the maps of South Asia"),
            ],style={"text-align": "center"}
        ),
        html.Div([
            html.H2("Description:"),
            html.P("The aim of this project is to visualize and digitalize the maps of South Asia for Indo Aryan language famiily."),
            html.P("Our project consist of majorly three parts-:"),
            html.Ul(
                children=[
                    html.Li(
                        "Indo-Aryan Language family tree"
                    ),
                    html.Li(
                        "Language wise analysis along with its spatial distribution and various dialects"
                    ),
                    html.Li(
                        "District wise analysis along with its corresponding state data"
                    )
                ]
            )
        ]),
        html.Div([
            html.H2("Instructor:"),
            # html.P("Chaithra Puttaswamy"),
            html.A("Chaithra Puttaswamy", href="https://www.iitk.ac.in/new/chaithra-puttaswamy")
            
        ]),
        html.Div(
            className="team-members",
            children=[
                html.H2("Team Members:"),
                html.Div(
                    className="members-grid",
                    children=[
                        html.Div(
                            children=[
                                html.A("Yash Gupta", href="https://linkedin.com/in/yashgupta0310")
                            ],
                            className="member",
                            
                        ),
                        html.Div(
                            children=[
                                html.A("Manan Kalavadia", href="https://linkedin.com/in/manan-kalavadia-a85219237")
                            ],
                            className="member"
                        ),
                        html.Div(
                            children=[
                                html.A("Abhishek Mishra",href="https://linkedin.com/in/abhishek-mishra-013786218")
                            ],
                            className="member"
                        ),
                        html.Div(
                            children=[
                                html.A("Divy Soni",href="https://linkedin.com/in/divy-soni-132249216")
                            ],
                            className="member"
                        ),
                    ],
                    style={
                        "display": "grid",
                        "grid-template-columns": "repeat(2, 1fr)",
                        "grid-gap": "10px",
                    },
                ),
            ],
        ),
        html.Div(
            className="github-link",
            children=[
                html.H2("Source Code: "),
                html.A("GitHub Repository", href="https://github.com/Yashgupta03/Eng448-Project"),
            ],
            style={
                "margin-top": "30px"
            }
        ),
        html.Div(
            className="References",
            children=[
                html.H2("References: "),
                html.Ul(
                        children=[
                            html.Li(
                                children=[
                                    "Lecture Notes of ENG-448, by Professor Chaithra Puttaswamy"
                                ]
                            ),
                            html.Li(
                                children=[
                                    html.A("Glottolog", href="https://glottolog.org/"),
                                ]
                            ),
                            html.Li(
                                children=[
                                    html.A("Wikipedia", href="https://en.wikipedia.org/wiki/Wiki"),
                                ]
                            ),
                        ]
                    ),
            ],
            style={
                "margin-top": "30px"
            }
        ),
    ],
    style={
        "font-family": "Arial",
        "font-size": "16px"
    },
)

