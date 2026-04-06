import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "../api/client";

type Application = {
  id: number;
  vacancy_id: number;
  vacancy_title: string;
  status: string;
  status_label: string;
};

export const MyApplicationsPage = () => {
  const { t, i18n } = useTranslation();
  const [applications, setApplications] = useState<Application[]>([]);

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const response = await api.get("/applications/my");
        setApplications(response.data.applications);
      } catch (error) {
        console.error("Error loading applications:", error);
      }
    };

    fetchApplications();
  }, [i18n.language]);

  return (
    <div style={{ padding: "20px" }}>
      <h2>{t("myApplications")}</h2>

      {applications.length === 0 ? (
        <p>{t("noApplications")}</p>
      ) : (
        applications.map((app) => (
          <div
            key={app.id}
            style={{
              border: "1px solid #ccc",
              borderRadius: "8px",
              padding: "16px",
              marginBottom: "12px",
            }}
          >
            <h3>{app.vacancy_title}</h3>
            <p>
              {t("status")}: {app.status_label}
            </p>
          </div>
        ))
      )}
    </div>
  );
};