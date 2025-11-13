using UnityEngine;

public class TeleportAnchor : MonoBehaviour
{
    public Transform teleportPoint;

    public Vector3 GetTeleportPosition()
    {
        return teleportPoint ? teleportPoint.position : transform.position;
    }
}
