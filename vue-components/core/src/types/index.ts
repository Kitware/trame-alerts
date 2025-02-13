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

export type PartialExcept<T, K extends keyof T> = Pick<T, K> &
  Partial<Omit<T, K>>;
export type AlertConstructor = PartialExcept<Omit<Alert, "id">, "type">;
export type AlertConstructorSpecialized = Partial<Omit<Alert, "id" | "type">>;
