"""Static versions of every review page, rendered together with the -s -a flags."""

from projects.showcase import theme_showcase as showcase


class ResearchTypography(showcase.ResearchThemeShowcase):
    def construct(self) -> None:
        self.add(self.typography_page())


class ResearchDarkTypography(showcase.ResearchDarkThemeShowcase):
    def construct(self) -> None:
        self.add(self.typography_page())


class EducationTypography(showcase.EducationThemeShowcase):
    def construct(self) -> None:
        self.add(self.typography_page())


class ResearchVisuals(showcase.ResearchThemeShowcase):
    def construct(self) -> None:
        self.add(self.visuals_page())


class ResearchDarkVisuals(showcase.ResearchDarkThemeShowcase):
    def construct(self) -> None:
        self.add(self.visuals_page())


class EducationVisuals(showcase.EducationThemeShowcase):
    def construct(self) -> None:
        self.add(self.visuals_page())


class ResearchExample(showcase.ResearchThemeShowcase):
    def construct(self) -> None:
        self.add(self.example_page())


class ResearchDarkExample(showcase.ResearchDarkThemeShowcase):
    def construct(self) -> None:
        self.add(self.example_page())


class EducationExample(showcase.EducationThemeShowcase):
    def construct(self) -> None:
        self.add(self.example_page())
