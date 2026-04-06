import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "../api/client";

type Vacancy = {
  id: number;
  title: string;
  description: string;
};

type ApplicationResponse = {
  message: string;
};

export const VacanciesPage = () => {
  const { t, i18n } = useTranslation();
  const [vacancies, setVacancies] = useState<Vacancy[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchVacancies = async () => {
      try {
        setLoading(true);
        const response = await api.get("/vacancies");
        setVacancies(response.data);
      } catch (error) {
        console.error("Error loading vacancies:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchVacancies();
  }, [i18n.language]);

  const handleApply = async (vacancyId: number) => {
    try {
      const response = await api.post<ApplicationResponse>("/apply", {
        vacancy_id: vacancyId,
      });
      setMessage(response.data.message);
    } catch (error) {
      console.error("Error applying:", error);
      setMessage("Something went wrong");
    }
  };

  if (loading) {
    return <h2>{t("loading")}</h2>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>{t("vacancies")}</h1>

      {message && (
        <div
          style={{
            marginBottom: "16px",
            padding: "12px",
            borderRadius: "8px",
            backgroundColor: "#e8f5e9",
            border: "1px solid #a5d6a7",
          }}
        >
          {message}
        </div>
      )}

      {vacancies.map((v) => (
        <div
          key={v.id}
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "16px",
            marginBottom: "12px",
          }}
        >
          <h3>{v.title}</h3>
          <p>{v.description}</p>
          <button className="btnApply" onClick={() => handleApply(v.id)}>{t("apply")}</button>
        </div>
      ))}
    </div>
  );
};