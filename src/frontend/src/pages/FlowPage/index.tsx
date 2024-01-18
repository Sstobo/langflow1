import { useContext, useEffect } from "react";
import { useParams } from "react-router-dom";
import Header from "../../components/headerComponent";
import { FlowsContext } from "../../contexts/flowsContext";
import Page from "./components/PageComponent";

export default function FlowPage(): JSX.Element {
  const { flows, tabId, setTabId, version } = useContext(FlowsContext);
  const { id } = useParams();

  // Set flow tab id
  useEffect(() => {
    setTabId(id!);
  }, [id]);

  return (
    <>
      <Header />
      <div className="flow-page-positioning">
        {flows.length > 0 &&
          tabId !== "" &&
          flows.findIndex((flow) => flow.id === tabId) !== -1 && (
            <Page flow={flows.find((flow) => flow.id === tabId)!} />
          )}
        <a
          target={"_blank"}
          href="https://logspace.ai/"
          className="logspace-page-icon"
        >
          {version && <div className="mt-1">⛓️ Langflow v{version}</div>}
          <div className={version ? "mt-2" : "mt-1"}>Created by Logspace</div>
        </a>
      </div>
    </>
  );
}
