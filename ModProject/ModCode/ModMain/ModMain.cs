using System;
using System.Reflection;
using HarmonyLib;
using UnityEngine;
using MOD_pzAi9g.Localization;

namespace MOD_pzAi9g
{
    public class ModMain
    {
        private const string HarmonyId = "MOD_pzAi9g";

        private Harmony harmony;
        private TimerCoroutine updateCoroutine;
        private int settingsProbeFrames;

        public void Init()
        {
            Debug.Log("[TL-Spanish] Init baseline-2026-08-27.");
            SpanishLocale.Load();

            harmony = new Harmony(HarmonyId);
            harmony.PatchAll(Assembly.GetExecutingAssembly());
            // Debug.Log("[TL-Spanish] Applied text localization patches. Press F8 to toggle Spanish for this session.");

            updateCoroutine = g.timer.Frame(new Action(OnUpdate), 1, true);
        }

        public void Destroy()
        {
            if (updateCoroutine != null)
                g.timer.Stop(updateCoroutine);

            if (harmony != null)
            {
                harmony.UnpatchSelf();
                harmony = null;
            }
        }

        private void OnUpdate()
        {
            settingsProbeFrames++;
            if (settingsProbeFrames >= 30)
            {
                settingsProbeFrames = 0;
                LanguageSelectorPatchState.ConfigureActiveSettings();
                SpanishLocale.ApplyHerdNpcNames();
            }

            // if (Input.GetKeyDown(KeyCode.F8))
            //     SpanishLocale.Toggle();
        }
    }
}
