import { useContext, useState } from "react";
import IconComponent from "../../components/genericIconComponent";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "../../components/ui/popover";
import { alertContext } from "../../contexts/alertContext";
import { AlertDropdownType } from "../../types/alerts";
import SingleAlert from "./components/singleAlertComponent";

export default function AlertDropdown({
  children,
}: AlertDropdownType): JSX.Element {
  const {
    notificationList,
    clearNotificationList,
    removeFromNotificationList,
    setNotificationCenter,
  } = useContext(alertContext);

  const [open, setOpen] = useState(false);

  return (
    <Popover
      open={open}
      onOpenChange={(target) => {
        setOpen(target);
        if (target) setNotificationCenter(false);
      }}
    >
      <PopoverTrigger>{children}</PopoverTrigger>
      <PopoverContent className="nocopy nopan nodelete nodrag noundo flex h-[500px] w-[500px] flex-col">
        <div className="text-md flex flex-row justify-between pl-3 font-medium text-foreground">
          Notifications
          <div className="flex gap-3 pr-3 ">
            <button
              className="text-foreground hover:text-status-red"
              onClick={() => {
                setOpen(false);
                setTimeout(clearNotificationList, 100);
              }}
            >
              <IconComponent name="Trash2" className="h-[1.1rem] w-[1.1rem]" />
            </button>
            <button
              className="text-foreground hover:text-status-red"
              onClick={() => {
                setOpen(false);
              }}
            >
              <IconComponent name="X" className="h-5 w-5" />
            </button>
          </div>
        </div>
        <div className="text-high-foreground mt-3 flex h-full w-full flex-col overflow-y-scroll scrollbar-hide">
          {notificationList.length !== 0 ? (
            notificationList.map((alertItem, index) => (
              <SingleAlert
                key={alertItem.id}
                dropItem={alertItem}
                removeAlert={removeFromNotificationList}
              />
            ))
          ) : (
            <div className="flex h-full w-full items-center justify-center pb-16 text-ring">
              No new notifications
            </div>
          )}
        </div>
      </PopoverContent>
    </Popover>
  );
}
