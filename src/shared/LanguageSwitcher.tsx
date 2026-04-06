import { useTranslation } from "react-i18next";

export const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const changeLang = (lang: string) => {
    i18n.changeLanguage(lang);
    localStorage.setItem("lang", lang);
  };

  return (
    <div style={{ padding: "20px", display: "flex", gap: "10px", justifyContent: "center" }}>
      <button className="btnLang" onClick={() => changeLang("en")}>EN</button>
      <button className="btnLang" onClick={() => changeLang("de")}>DE</button>
      <button className="btnLang" onClick={() => changeLang("ru")}>RU</button>
    </div>
  );
};