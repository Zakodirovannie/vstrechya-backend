import React, { createContext, ReactNode, useContext, useState, useEffect } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { AuthContext } from "./AuthContext";

const DefaultProps = {
  unreadMessageCount: 0,
  connectionStatus: "Uninstantiated",
};

export interface NotificationProps {
  unreadMessageCount: number;
  connectionStatus: string;
}

export const NotificationContext =
  createContext<NotificationProps>(DefaultProps);

export const NotificationContextProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const { user } = useContext(AuthContext);
  const [unreadMessageCount, setUnreadMessageCount] = useState(0);

  async function fetchAuthToken() {
    try {
        const response = await fetch('http://127.0.0.1:8000/auth/wslogin', {
          headers: {
            Authorization: `Bearer ${user?.token}`,
          },
        });
        const data = await response.json();
        return data.uuid; // Предположим, что возвращаемый объект имеет свойство token
    } catch (error) {
        console.error('Error fetching auth token:', error);
        return ''; // В случае ошибки возвращаем пустую строку или другое значение по умолчанию
    }
  }

  const [authToken, setAuthToken] = useState('');

    useEffect(() => {
        const fetchToken = async () => {
            const token = await fetchAuthToken();
            setAuthToken(token);
        };

        fetchToken();
    }, []);

  const { readyState } = useWebSocket(
    user ? `ws://127.0.0.1:8000/notifications/` : null,
    {
      queryParams: {
        uuid: user ? authToken : "",
      },
      onOpen: () => {
        console.log("Connected to Notifications!");
      },
      onClose: () => {
        console.log("Disconnected from Notifications!");
      },
      onMessage: (e) => {
        const data = JSON.parse(e.data);
        switch (data.type) {
          case "unread_count":
            setUnreadMessageCount(data.unread_count);
            break;
          case "new_message_notification":
            setUnreadMessageCount((count) => (count += 1));
            break;
          default:
            console.error("Unknown message type!");
            break;
        }
      },
    }
  );

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  return (
    <NotificationContext.Provider
      value={{ unreadMessageCount, connectionStatus }}
    >
      {children}
    </NotificationContext.Provider>
  );
};
