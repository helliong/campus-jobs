import { VacanciesPage } from "./pages/VacanciesPage";
import { MyApplicationsPage } from "./pages/MyApplicationsPage";
import { LanguageSwitcher } from "./shared/LanguageSwitcher";
import "./App.css";

function App() {
  return (
    <div>
      <LanguageSwitcher />
      <VacanciesPage />
      <MyApplicationsPage />
    </div>
  );
}

export default App;