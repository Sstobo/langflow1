import { useContext, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import PaginatorComponent from "../../../../components/PaginatorComponent";
import CollectionCardComponent from "../../../../components/cardComponent";
import CardsWrapComponent from "../../../../components/cardsWrapComponent";
import IconComponent from "../../../../components/genericIconComponent";
import { SkeletonCardComponent } from "../../../../components/skeletonCardComponent";
import { Button } from "../../../../components/ui/button";
import { alertContext } from "../../../../contexts/alertContext";
import { FlowsContext } from "../../../../contexts/flowsContext";
import { FlowType } from "../../../../types/flow";

export default function ComponentsComponent({
  is_component = true,
}: {
  is_component?: boolean;
}) {
  const { flows, removeFlow, uploadFlow, addFlow, isLoading } =
    useContext(FlowsContext);
  const { setErrorData, setSuccessData } = useContext(alertContext);
  const [pageSize, setPageSize] = useState(10);
  const [pageIndex, setPageIndex] = useState(1);
  const [loadingScreen, setLoadingScreen] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    if (isLoading) return;
    const all = flows
      .filter((f) => (f.is_component ?? false) === is_component)
      .sort((a, b) => {
        if (a?.updated_at && b?.updated_at) {
          return (
            new Date(b?.updated_at!).getTime() -
            new Date(a?.updated_at!).getTime()
          );
        } else if (a?.updated_at && !b?.updated_at) {
          return 1;
        } else if (!a?.updated_at && b?.updated_at) {
          return -1;
        } else {
          return (
            new Date(b?.date_created!).getTime() -
            new Date(a?.date_created!).getTime()
          );
        }
      });
    const start = (pageIndex - 1) * pageSize;
    const end = start + pageSize;
    setData(all.slice(start, end));
  }, [flows, pageIndex, pageSize]);

  const [data, setData] = useState<FlowType[]>([]);

  const name = is_component ? "Component" : "Flow";

  const onFileDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.types.some((types) => types === "Files")) {
      if (e.dataTransfer.files.item(0).type === "application/json") {
        uploadFlow({
          newProject: true,
          file: e.dataTransfer.files.item(0)!,
          isComponent: is_component,
        })
          .then(() => {
            setSuccessData({
              title: `${
                is_component ? "Component" : "Flow"
              } uploaded successfully`,
            });
          })
          .catch((error) => {
            setErrorData({
              title: "Error uploading file",
              list: [error],
            });
          });
      } else {
        setErrorData({
          title: "Invalid file type",
          list: ["Please upload a JSON file"],
        });
      }
    }
  };

  function resetFilter() {
    setPageIndex(1);
    setPageSize(10);
  }

  useEffect(() => {
    setTimeout(() => {
      setLoadingScreen(false);
    }, 600);
  }, []);

  return (
    <CardsWrapComponent
      onFileDrop={onFileDrop}
      dragMessage={`Drag your ${name} here`}
    >
      <div className="flex h-full w-full flex-col justify-between">
        <div className="flex w-full flex-col gap-4">
          {!loadingScreen && data.length === 0 ? (
            <div className="mt-6 flex w-full items-center justify-center text-center">
              <div className="flex-max-width h-full flex-col">
                <div className="flex w-full flex-col gap-4">
                  <div className="grid w-full gap-4">
                    Flows and components can be created using Langflow.
                  </div>
                  <div className="align-center flex w-full justify-center gap-1">
                    <span>New?</span>
                    <span className="transition-colors hover:text-muted-foreground">
                      <button
                        onClick={() => {
                          addFlow(true).then((id) => {
                            navigate("/flow/" + id);
                          });
                        }}
                        className="underline"
                      >
                        Start Here
                      </button>
                      .
                    </span>
                    <span className="animate-pulse">🚀</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="grid w-full gap-4 md:grid-cols-2 lg:grid-cols-2">
              {loadingScreen === false && data?.length > 0 ? (
                data?.map((item, idx) => (
                  <CollectionCardComponent
                    onDelete={() => {
                      removeFlow(item.id);
                      setSuccessData({
                        title: `${
                          item.is_component ? "Component" : "Flow"
                        } deleted successfully!`,
                      });
                      resetFilter();
                    }}
                    key={idx}
                    data={item}
                    disabled={isLoading}
                    button={
                      !is_component ? (
                        <Link to={"/flow/" + item.id}>
                          <Button
                            tabIndex={-1}
                            variant="outline"
                            size="sm"
                            className="whitespace-nowrap "
                          >
                            <IconComponent
                              name="ExternalLink"
                              className="main-page-nav-button select-none"
                            />
                            Edit Flow
                          </Button>
                        </Link>
                      ) : (
                        <></>
                      )
                    }
                  />
                ))
              ) : (
                <>
                  <SkeletonCardComponent />
                  <SkeletonCardComponent />
                </>
              )}
            </div>
          )}
        </div>
        {!loadingScreen && data.length > 0 && (
          <div className="relative py-6">
            <PaginatorComponent
              storeComponent={true}
              pageIndex={pageIndex}
              pageSize={pageSize}
              rowsCount={[10, 20, 50, 100]}
              totalRowsCount={
                flows.filter((f) => (f.is_component ?? false) === is_component)
                  .length
              }
              paginate={(pageSize, pageIndex) => {
                setPageIndex(pageIndex);
                setPageSize(pageSize);
              }}
            ></PaginatorComponent>
          </div>
        )}
      </div>
    </CardsWrapComponent>
  );
}
