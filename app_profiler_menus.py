import streamlit as st
import altair as alt
import pandas as pd
import bibtexparser
from rapidfuzz import fuzz
from pylatexenc.latex2text import LatexNodes2Text
latex_to_text = LatexNodes2Text().latex_to_text
import base64

st.set_page_config(
	page_title="HEP Research Profile",
	layout="wide"
)

st.sidebar.title("Navigation")
menu = st.sidebar.radio(
	"Go to:",
	["Researcher Profile", "Literature"],
)

# Dummy data

physics_data = pd.DataFrame({
	"Experiment": ["Alpha Decay", "Beta Decay", "Gamma Ray Analysis", "Quark Study", "Higgs Boson"],
	"Energy (MeV)": [4.2, 1.5, 2.9, 3.4, 7.1],
	"Date": pd.date_range(start="2024-01-01", periods=5),
})

astronomy_data = pd.DataFrame({
	"Celestial Object": ["Mars", "Venus", "Jupiter", "Saturn", "Moon"],
	"Brightness (Magnitude)": [-2.0, -4.6, -1.8, 0.2, -12.7],
	"Observation Date": pd.date_range(start="2024-01-01", periods=5),
})

weather_data = pd.DataFrame({
	"City": ["Cape Town", "London", "New York", "Tokyo", "Sydney"],
	"Temperature (°C)": [25, 10, -3, 15, 30],
	"Humidity (%)": [65, 70, 55, 80, 50],
	"Recorded Date": pd.date_range(start="2024-01-01", periods=5),
})

def format_author(name: str) -> str:

	if name.strip().lower() == "others":
		return ""
	
	if "," in name:
		last, firsts = name.split(",", 1)
		initials = " ".join(f"{f[0]}." for f in
							firsts.split() if f)
		return f"{initials} {last.strip()}"
	
	else:
		parts = name.split()
		initials = " ".join(f"{p[0]}." for p
							in parts[:-1])
		return f"{initials} {parts[-1]}"

def format_authors(author_field: str) -> str:

	if not isinstance(author_field, str):
		return ""

	raw_authors = [a.strip() for a in
				   author_field.split(" and ")]

	has_others = any(a.lower() == "others"
					 for a in raw_authors)

	formatted = []
	for a in raw_authors:
		fa = format_author(a)
		if fa:
			formatted.append(fa)

	if has_others or len(formatted) > 4:
		shown = formatted[:4]
		return ", ".join(shown) + " et al."

	if len(formatted) <= 2:
		return " and ".join(formatted)

	return ", ".join(formatted[:-1])+" and "+formatted[-1]

def first_author_surname(author_str: str) -> str:

	if not (isinstance(author_str, str) and author_str.strip()):
		return ""
	
	author_str = (
		author_str
		.replace(" et al.", "")
		.replace(" and", ",")
		.strip()
	)

	first_author = author_str.split(",")[0]

	return first_author.split()[-1].lower()

def row_matches(row, keyword, threshold=90):
	keyword = str(keyword).lower()
	for val in row:
		val_str = str(val).lower()
		if fuzz.partial_ratio(keyword, val_str) >= threshold:
			return True
	return False

# Sections based on menu selection
if menu == "Researcher Profile":

	st.title("Researcher Profile")

	# Collect basic information
	name = "Jack Brand"
	institution = "Department of Physics, University of Cape Town"
	email = "74jdvb@gmail.com"

	st.write(
		f"""
		<div style="text-align: center;">
		<div style="font-size: 1.2em;">
			{name}<br>
		</div>
		<a href="{email}">
			{email}
		</a><br>
		{institution}<br>
		</div><br>
		""",
		unsafe_allow_html=True
	)
	st.markdown(
		"""
		I am a Physics graduate student specializing in high energy physics phenomenology (hep-ph). My research concerns an exotic state of matter called the quark-gluon plasma. But what, pray tell, is the quark-gluon plasma?

		As you may know, the majority of matter that you see or interact with is made of atoms. Leucippus, in the 5th century BCE, and other ancient philosophers, posited that matter was comprised of fundamental indivisble components called atoms. On the contrary, we can indeed divide atoms, as we have defined them, into distinguishable parts. An atom comprises an outer cloud of electrons and a central nucleus of protons and neutrons.
		
		Protons and neutrons are examples of what we call hadrons. They are bound together in the nucleus by what we term the weak nuclear force. As it turns out, hadrons are comprised of yet smaller particles, called quarks and gluons, bound together by what we term the strong nuclear force. Within the Standard Model of physics, quarks, gluons and electrons, along with a few others, are fundamental, indivisible particles -- there is a Nobel prize waiting for you if you disprove this!
		"""
	)
	st.write(
    	"""
		<br>
    	<div style="
			width: 600px;
			height: 625px;
			overflow: hidden;
			margin: 0 auto;
			position: relative;
		">
        	<img
            	src="https://irfu.cea.fr/Images/astImg/610_1.jpg"
            	style="
					position: relative;
                	top: -10px;
                	left: -15px;
					width: auto;
					height: auto
            	"
        	>
    	</div>
    	""",
    	unsafe_allow_html=True
	)
	st.write(
		"""
		<div style="margin-left: 75px; margin-right: 75px;">
			<div style="font-size: 0.8em; text-align: center; margin-bottom: 1em;">
				Credit: 
				<a href="https://animalia-life.club/qa/pictures/quark-gluon-plasma-phase-diagram">
					https://animalia-life.club/qa/pictures/quark-gluon-plasma-phase-diagram
				</a>
			</div>
			<b>Fig. 1:</b>
			Phase diagram of matter interacting via the strong nuclear force.
			Quarks and gluons are fundamental particles that are bound together in states called hadrons.
			If a hadron has three quarks in it, we call it a baryon; if it has two quarks in it, we call it a meson.
		</div>
		<br>
		""",
		unsafe_allow_html=True
	)
	st.markdown(
		"""
		As the name might suggest, the strong nuclear force is incredibly strong. It works only on very small scales, but takes an immense amount of energy to overcome. This is why we must collide nuclei at great speeds in particle colliders -- such as the Large Hadron Collier (LHC) or Relativistic Heavy Ion Collider (RHIC) -- in order to study the strong nuclear force. It is theorised, and well supported by evidence, that for a very brief time (one billionth of a second) after such a collision, the quarks and gluons that make up protons and neutrons become unbound, forming an extremely hot fluid-like state called the quark-gluon plasma (QGP), or as I call it, particle soup.

		A lot of work has been done in order to find under which conditions the change from bound hadronic matter to unbound quark-gluon plasma occurs. The physics community is mostly agreed that we've observed a QGP when we've collided very big nuclei, like lead nuclei, but haven't observed a QGP when colliding the smallest nuclei, namely hydrogen  nuclei (which are just single protons). Recently, in 2025, we collided oxygen nuclei at the LHC, and evidence is emerging from ongoing data analysis that a QGP formed! Using theoretical modelling and computation, my researach group continues to push the question: Can we go smaller?
		"""
	)

elif menu == "Literature":

	st.title("Literature")
	st.write("The following is a collection of high energy physics (HEP) literature that I referenced in my BSc (Hons) research project. Feel free to explore!")

	with open("publications.bib") as f:
		bib_database = bibtexparser.load(f)

	publications = (
		pd.DataFrame(bib_database.entries)
		.filter(items=["author","collaboration","title","year","journal","doi"])
	)

	publications.columns = publications.columns.str.title()

	publications = publications.rename(columns={"Doi": "DOI"})

	publications["Author"] = (
		publications["Author"]
		.apply(format_authors)
		.apply(latex_to_text)
	)

	publications["Title"] = (
		publications["Title"]
		.apply(latex_to_text)
	)

	publications["First Author Surname"] = (
		publications["Author"]
		.apply(first_author_surname)
	)
	publications = publications.sort_values(
		by=["First Author Surname", "Year"],
		ascending=[True, True]
	)
	publications = publications.drop(columns="First Author Surname")
	
	years = (
		pd.to_numeric(publications["Year"], errors="coerce")
		.dropna()
		.astype(int)
	)

	year_range = range(years.min(), years.max() + 1)

	counts = (
		years
		.value_counts()
		.sort_index()
		.reindex(year_range, fill_value=0)
	)

	publications["DOI"] = publications["DOI"].apply(
    	lambda doi: f"https://doi.org/{doi}"
		if pd.notna(doi) and doi else ""
	)

	keyword = st.text_input("", icon="🔍", placeholder="Search")

	if keyword:
		filtered = publications[publications.apply(
			lambda row:
			row_matches(
				row.drop(labels=["DOI"], 
						 errors="ignore"),
				keyword
			),
			axis=1
		)]
		st.dataframe(
			filtered,
			hide_index=True
		)
		filtered_years = (
			pd.to_numeric(filtered["Year"], errors="coerce")
			.dropna()
			.astype(int)
		)
		filtered_counts = (
			filtered_years
			.value_counts()
			.sort_index()
			.reindex(year_range, fill_value=0)
		)
		histogram_df = pd.DataFrame({
			f'Filtered by "{keyword}"': filtered_counts,
			"All publications": counts - filtered_counts
		}, index=year_range)

	else:
		st.dataframe(
			publications,
			hide_index=True,
			column_config={
				"DOI": st.column_config.LinkColumn()
			},
			use_container_width=True
		)
		histogram_df = pd.DataFrame({
			"All publications": counts
		}, index=year_range)
	
	histogram = histogram_df.reset_index().melt(
		id_vars="index",
		var_name="Category",
		value_name="Count"
	).rename(columns={"index": "Year"})

	chart = alt.Chart(histogram).mark_bar().encode(
		x=alt.X(
			'Year:O',
			title='Year'
		),
		y=alt.Y(
			'Count:Q',
			title='Number of publications'
		),
		color=alt.Color(
			'Category:N',
			legend=(
				alt.Legend(orient="top", title=None)
				if keyword else None
			)
		)
	)

	st.altair_chart(chart, use_container_width=True)

elif menu == "Data Explorer":
	st.title("Data Explorer")
	st.sidebar.header("Data Selection")

	data_option = st.sidebar.selectbox(
		"Choose a dataset to explore",
		["Physics Experiments", "Astronomy Observations", "Weather Data"]
	)

	if data_option == "Physics Experiments":
		st.write("### Physics Experiment Data")
		st.dataframe(physics_data)
		energy_filter = st.slider(
			"Filter by Energy (MeV)", 0.0, 10.0, (0.0, 10.0))
		filtered_physics = physics_data[
			physics_data["Energy (MeV)"].between(
				energy_filter[0], energy_filter[1])
		]
		st.write(f"Filtered Results for Energy Range {energy_filter}:")
		st.dataframe(filtered_physics)

	elif data_option == "Astronomy Observations":
		st.write("### Astronomy Observation Data")
		st.dataframe(astronomy_data)
		brightness_filter = st.slider(
			"Filter by Brightness (Magnitude)", -15.0, 5.0, (-15.0, 5.0))
		filtered_astronomy = astronomy_data[
			astronomy_data["Brightness (Magnitude)"].between(
				brightness_filter[0], brightness_filter[1])
		]
		st.write(f"Filtered Results for Brightness Range {brightness_filter}:")
		st.dataframe(filtered_astronomy)

	elif data_option == "Weather Data":
		st.write("### Weather Data")
		st.dataframe(weather_data)
		temp_filter = st.slider("Filter by Temperature (°C)", -10.0, 40.0, (-10.0, 40.0))
		humidity_filter = st.slider("Filter by Humidity (%)", 0, 100, (0, 100))
		filtered_weather = weather_data[
			weather_data["Temperature (°C)"].between(temp_filter[0], temp_filter[1]) &
			weather_data["Humidity (%)"].between(
				humidity_filter[0], humidity_filter[1])
		]
		st.write(f"Filtered Results for Temperature {temp_filter} and Humidity {humidity_filter}:")
		st.dataframe(filtered_weather)
