import "./components.css";

type UserBubbleProps = {
  message: string;
};

export default function UserBubble({ message }: UserBubbleProps) {
  return (
    <div className="w-full flex justify-end">
      <div className="bubble user-bubble">{message}</div>
    </div>
  );
}
