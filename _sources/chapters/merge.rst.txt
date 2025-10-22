Merge próbálkozás
=================

.. plantuml::
    :align: center
    :caption: Steam Dataset Merge Process

    @startuml
    title Steam Dataset Merge Process
    skinparam defaultFontName Arial

    skinparam activity {
        BackgroundColor<<Source>> LightBlue
        BackgroundColor<<Intermediate>> LightYellow
        BackgroundColor<<Output>> LightGreen
    }

    start

    partition "Source A" <<Source>> {
        :load_source_a() -> a;
        :Clean & normalize columns;
        :Merge CSVs;
    }

    partition "Source B" <<Source>> {
        :load_source_b(B_PATH) -> b;
        :JSON to DataFrame;
        :Convert numeric & bool columns;
    }

    partition "Source C" <<Source>> {
        :load_source_c() -> c;
        :Clean & normalize columns;
        :Concatenate CSVs;
    }

    partition "Intermediate" <<Intermediate>> {
        :merge_sources(a, b, c) -> d;
        :analyze_name_matches(d);
        :analyze_multi_source_attribute(d, attr) [for genre, category, language, developer, publisher];
        :Generate release year Gantt chart;
        :Check duplicated appids;
        :finalize_dataset(d) -> final;
    }

    partition "Output" <<Output>> {
        :save_output(final);
    }

    stop
    @enduml