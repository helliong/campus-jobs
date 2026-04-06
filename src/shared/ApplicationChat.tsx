import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api } from "../api/client";

type Message = {
  id: number;
  application_id: number;
  sender: "student" | "employer";
  text: string;
};

type ApplicationChatProps = {
  applicationId: number;
};

export const ApplicationChat = ({ applicationId }: ApplicationChatProps) => {
  const { t, i18n } = useTranslation();
  const [messages, setMessages] = useState<Message[]>([]);
  const [text, setText] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const fetchMessages = async () => {
    try {
      const response = await api.get(`/applications/${applicationId}/messages`);
      setMessages(response.data.messages);
    } catch (error) {
      console.error("Error loading messages:", error);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchMessages();
    }
  }, [isOpen, i18n.language]);

  const handleSend = async (sender: "student" | "employer") => {
    if (!text.trim()) return;

    try {
      await api.post(`/applications/${applicationId}/messages`, {
        sender,
        text,
      });

      setText("");
      fetchMessages();
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div style={{ marginTop: "12px" }}>
      <button onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? t("closeChat") : t("openChat")}
      </button>

      {isOpen && (
        <div
          style={{
            marginTop: "12px",
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "12px",
          }}
        >
          <h4>{t("messages")}</h4>

          {messages.length === 0 ? (
            <p>{t("noMessages")}</p>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                style={{
                  marginBottom: "8px",
                  padding: "8px",
                  borderRadius: "6px",
                  backgroundColor:
                    message.sender === "student" ? "#e3f2fd" : "#f3e5f5",
                }}
              >
                <strong>
                  {message.sender === "student" ? t("student") : t("employer")}
                </strong>
                <p style={{ margin: "4px 0 0" }}>{message.text}</p>
              </div>
            ))
          )}

          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={t("writeMessage")}
            style={{
              width: "100%",
              padding: "10px",
              marginTop: "12px",
              marginBottom: "8px",
              boxSizing: "border-box",
            }}
          />

          <div style={{ display: "flex", gap: "8px" }}>
            <button onClick={() => handleSend("student")}>{t("student")}</button>
            <button onClick={() => handleSend("employer")}>{t("employer")}</button>
          </div>
        </div>
      )}
    </div>
  );
};