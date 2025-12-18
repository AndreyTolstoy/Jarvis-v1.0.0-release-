from Panel.jsons import load
    

def plugin_run(plugins : list, plugins_args : dict, config : dict):
        if "ats" in config and config["ats"] != False or not config:
         if plugins != []:
            for plugin_name in plugins:
                 plugin_code = load("jsons_data/data.json")["plugins"][plugin_name]["data"]
                 if plugin_code:
                   bridge(plugin_code, plugins_args, config)
                   print(f"ATS v5.0 {plugin_name} ✅")

        else:
           print("ATS v5.0 can`t run plugin: ats disabled in control panel")


def bridge(code, plugin_params, config):
 from ATS_v5.main import ElementsSpliter
 ElementsSpliter().main(code, plugin_params, config)