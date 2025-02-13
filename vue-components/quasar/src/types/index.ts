export type AlertType = "error" | "warning" | "success" | "info";

export type Alert = {
  id: number;
  type: AlertType;
  title: string;
  text: string;
  timeout: number;
  elapsed: boolean;
  persistent: boolean;
};
