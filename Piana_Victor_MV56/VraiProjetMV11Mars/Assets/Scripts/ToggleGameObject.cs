using UnityEngine;

public class ToggleGameObject : MonoBehaviour
{
    public GameObject target;

    public void Toggle()
    {
        if (target != null)
        {
            target.SetActive(!target.activeSelf);
        }
    }
}
