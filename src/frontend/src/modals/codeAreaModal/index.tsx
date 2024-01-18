import "ace-builds/src-noconflict/ace";
import "ace-builds/src-noconflict/ext-language_tools";
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/theme-twilight";
// import "ace-builds/webpack-resolver";
import { useContext, useEffect, useState } from "react";
import AceEditor from "react-ace";
import IconComponent from "../../components/genericIconComponent";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { CODE_PROMPT_DIALOG_SUBTITLE } from "../../constants/constants";
import { alertContext } from "../../contexts/alertContext";
import { darkContext } from "../../contexts/darkContext";
import { typesContext } from "../../contexts/typesContext";
import { postCustomComponent, postValidateCode } from "../../controllers/API";
import { codeAreaModalPropsType } from "../../types/components";
import BaseModal from "../baseModal";

export default function CodeAreaModal({
  value,
  setValue,
  nodeClass,
  setNodeClass,
  children,
  dynamic,
  readonly = false,
}: codeAreaModalPropsType): JSX.Element {
  const [code, setCode] = useState(value);
  const { dark } = useContext(darkContext);
  const { reactFlowInstance } = useContext(typesContext);
  const [height, setHeight] = useState<string | null>(null);
  const { setErrorData, setSuccessData } = useContext(alertContext);
  const [error, setError] = useState<{
    detail: { error: string | undefined; traceback: string | undefined };
  } | null>(null);

  useEffect(() => {
    // if nodeClass.template has more fields other than code and dynamic is true
    // do not run handleClick
    if (dynamic && Object.keys(nodeClass!.template).length > 2) {
      return;
    }
  }, []);

  function processNonDynamicField() {
    postValidateCode(code)
      .then((apiReturn) => {
        if (apiReturn.data) {
          let importsErrors = apiReturn.data.imports.errors;
          let funcErrors = apiReturn.data.function.errors;
          if (funcErrors.length === 0 && importsErrors.length === 0) {
            setSuccessData({
              title: "Code is ready to run",
            });
            setOpen(false);
            setValue(code);
            // setValue(code);
          } else {
            if (funcErrors.length !== 0) {
              setErrorData({
                title: "There is an error in your function",
                list: funcErrors,
              });
            }
            if (importsErrors.length !== 0) {
              setErrorData({
                title: "There is an error in your imports",
                list: importsErrors,
              });
            }
          }
        } else {
          setErrorData({
            title: "Something went wrong, please try again",
          });
        }
      })
      .catch((_) => {
        setErrorData({
          title: "There is something wrong with this code, please review it",
        });
      });
  }

  function processDynamicField() {
    postCustomComponent(code, nodeClass!)
      .then((apiReturn) => {
        const { data } = apiReturn;
        if (data) {
          setNodeClass(data, code);
          setError({ detail: { error: undefined, traceback: undefined } });
          setOpen(false);
        }
      })
      .catch((err) => {
        setError(err.response.data);
      });
  }

  function processCode() {
    if (!dynamic) {
      processNonDynamicField();
    } else {
      processDynamicField();
    }
  }

  function handleClick() {
    processCode();
  }

  useEffect(() => {
    // Function to be executed after the state changes
    const delayedFunction = setTimeout(() => {
      if (error?.detail.error !== undefined) {
        //trigger to update the height, does not really apply any height
        setHeight("90%");
      }
      //600 to happen after the transition of 500ms
    }, 600);

    // Cleanup function to clear the timeout if the component unmounts or the state changes again
    return () => {
      clearTimeout(delayedFunction);
    };
  }, [error, setHeight]);

  const [open, setOpen] = useState(false);

  useEffect(() => {
    setCode(value);
  }, [value, open]);

  return (
    <BaseModal open={open} setOpen={setOpen}>
      <BaseModal.Trigger>{children}</BaseModal.Trigger>
      <BaseModal.Header description={CODE_PROMPT_DIALOG_SUBTITLE}>
        <span className="pr-2">Edit Code</span>
        <IconComponent
          name="prompts"
          className="h-6 w-6 pl-1 text-primary "
          aria-hidden="true"
        />
      </BaseModal.Header>
      <BaseModal.Content>
        <Input
          value={code}
          className="absolute left-[500%] top-[500%]"
          id="codeValue"
        />
        <div className="flex h-full w-full flex-col transition-all">
          <div className="h-full w-full">
            <AceEditor
              readOnly={readonly}
              value={code}
              mode="python"
              height={height ?? "100%"}
              highlightActiveLine={true}
              showPrintMargin={false}
              fontSize={14}
              showGutter
              enableLiveAutocompletion
              theme={dark ? "twilight" : "github"}
              name="CodeEditor"
              onChange={(value) => {
                setCode(value);
              }}
              className="h-full w-full rounded-lg border-[1px] border-gray-300 custom-scroll dark:border-gray-600"
            />
          </div>
          <div
            className={
              "whitespace-break-spaces transition-all delay-500" +
              (error?.detail?.error !== undefined ? "h-2/6" : "h-0")
            }
          >
            <div className="mt-1 h-full max-h-[10rem] w-full overflow-y-auto overflow-x-clip text-left custom-scroll">
              <h1 className="text-lg text-destructive">
                {error?.detail?.error}
              </h1>
              <div className="ml-2 w-full text-sm text-status-red word-break-break-word">
                <span className="w-full word-break-break-word">
                  {error?.detail?.traceback}
                </span>
              </div>
            </div>
          </div>
          <div className="flex h-fit w-full justify-end">
            <Button
              className="mt-3"
              onClick={handleClick}
              type="submit"
              id="checkAndSaveBtn"
              disabled={readonly}
            >
              Check & Save
            </Button>
          </div>
        </div>
      </BaseModal.Content>
    </BaseModal>
  );
}
